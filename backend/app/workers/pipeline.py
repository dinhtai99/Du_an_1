import asyncio
import uuid
from pathlib import Path

from app.core.config import settings
from app.providers.google_flow.client import (
    FlowUserActionRequired,
    GoogleFlowClient,
)
from app.providers.tts.edge import EdgeTTSService
from app.schemas.pipeline import PipelineJobResponse, PipelineStartRequest
from app.services.job_store import JobStore
from app.services.script_planner import ScriptPlanner
from app.services.video_renderer import VideoRenderer


class PipelineWorker:
    def __init__(self) -> None:
        self.store = JobStore()
        self.planner = ScriptPlanner()
        self.flow = GoogleFlowClient()
        self.tts = EdgeTTSService()
        self.renderer = VideoRenderer()
        self._tasks: dict[str, asyncio.Task] = {}
        self._run_lock = asyncio.Lock()

    async def start(self, request: PipelineStartRequest) -> PipelineJobResponse:
        job_id = str(uuid.uuid4())
        project_dir = self.store.create_project_dir(job_id)
        job = PipelineJobResponse(
            id=job_id,
            title=request.title or request.topic,
            topic=request.topic,
            project_dir=str(project_dir),
            request=request,
            scenes=self.planner.create_scenes(request),
        )
        self.store.save(job)
        self._schedule(job_id)
        return job

    async def resume(self, job_id: str) -> PipelineJobResponse:
        job = self.store.load(job_id)
        existing = self._tasks.get(job_id)
        if existing and not existing.done():
            return job
        job.status = "pending"
        job.error_message = None
        job.user_action_prompt = None
        self.store.save(job)
        self._schedule(job_id)
        return job

    def get(self, job_id: str) -> PipelineJobResponse:
        return self.store.load(job_id)

    def list_recent(self) -> list[PipelineJobResponse]:
        return self.store.list_recent()

    async def close(self) -> None:
        for task in self._tasks.values():
            if not task.done():
                task.cancel()
        await self.flow.close()

    def _schedule(self, job_id: str) -> None:
        task = asyncio.create_task(self._run(job_id))
        self._tasks[job_id] = task
        task.add_done_callback(lambda _: self._tasks.pop(job_id, None))

    async def _run(self, job_id: str) -> None:
        async with self._run_lock:
            job = self.store.load(job_id)
            job.status = "running"
            job.current_step = "Chuẩn bị các cảnh"
            self.store.save(job)
            total_units = max(len(job.scenes) * 2 + (1 if job.request.render_video else 0), 1)
            completed_units = sum(1 for scene in job.scenes if self._has_file(scene.image_path))
            completed_units += sum(1 for scene in job.scenes if self._has_file(scene.audio_path))

            try:
                for scene in job.scenes:
                    if self._has_file(scene.image_path):
                        continue
                    if not job.request.generate_images:
                        raise RuntimeError(
                            f"Cảnh {scene.order} chưa có image_path và chế độ tạo ảnh đã tắt."
                        )

                    scene.status = "generating"
                    job.current_step = f"Google Flow đang tạo ảnh cảnh {scene.order}/{len(job.scenes)}"
                    self.store.save(job)
                    image_path = await self.flow.generate_image(
                        prompt=scene.image_prompt,
                        destination_dir=Path(job.project_dir) / "images",
                        scene_order=scene.order,
                    )
                    scene.image_path = str(image_path)
                    scene.status = "completed"
                    completed_units += 1
                    self._set_progress(job, completed_units, total_units)

                for scene in job.scenes:
                    if self._has_file(scene.audio_path) and self._has_file(scene.subtitle_path):
                        continue
                    scene.status = "generating"
                    job.current_step = f"Đang tạo giọng đọc cảnh {scene.order}/{len(job.scenes)}"
                    self.store.save(job)
                    audio_path = Path(job.project_dir) / "audio" / f"scene_{scene.order:03d}.mp3"
                    subtitle_path = (
                        Path(job.project_dir) / "subtitles" / f"scene_{scene.order:03d}.srt"
                    )
                    await self.tts.synthesize(
                        text=scene.narration,
                        audio_path=audio_path,
                        subtitle_path=subtitle_path,
                        voice=job.request.voice,
                    )
                    scene.audio_path = str(audio_path)
                    scene.subtitle_path = str(subtitle_path)
                    scene.status = "completed"
                    completed_units += 1
                    self._set_progress(job, completed_units, total_units)

                if job.request.render_video:
                    job.current_step = "Đang ghép video bằng FFmpeg"
                    self.store.save(job)
                    output_path = settings.EXPORTS_DIR / f"{job.id}.mp4"
                    await self.renderer.render(
                        scenes=job.scenes,
                        output_path=output_path,
                        logo_path=job.request.logo_path,
                    )
                    job.output_video_path = str(output_path)
                    job.output_video_url = f"/media/{output_path.name}"
                    completed_units += 1

                job.status = "completed"
                job.current_step = "Hoàn tất"
                job.progress_percent = 100
                job.user_action_prompt = None
                self.store.save(job)
            except FlowUserActionRequired as exc:
                job.status = "waiting_for_user"
                job.current_step = "Đang chờ thao tác trên Google Flow"
                job.user_action_prompt = str(exc)
                self.store.save(job)
            except asyncio.CancelledError:
                raise
            except Exception as exc:
                job.status = "failed"
                job.current_step = "Tác vụ thất bại"
                job.error_message = str(exc)
                self.store.save(job)

    def _set_progress(
        self,
        job: PipelineJobResponse,
        completed_units: int,
        total_units: int,
    ) -> None:
        job.progress_percent = round(completed_units / total_units * 100, 1)
        self.store.save(job)

    @staticmethod
    def _has_file(value: str | None) -> bool:
        return bool(value and Path(value).is_file())
