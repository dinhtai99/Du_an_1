import json
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path

from app.core.config import settings
from app.schemas.pipeline import PipelineJobResponse


class JobStore:
    def create_project_dir(self, job_id: str, title: str) -> Path:
        normalized = unicodedata.normalize("NFKD", title)
        ascii_title = normalized.encode("ascii", "ignore").decode("ascii")
        slug = re.sub(r"[^a-z0-9]+", "-", ascii_title.lower()).strip("-")
        slug = slug[:60] or "kich-ban"
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        project_dir = settings.PROJECTS_DIR / f"{timestamp}-{slug}--{job_id}"
        for name in ("images", "audio", "subtitles", "debug", "video"):
            (project_dir / name).mkdir(parents=True, exist_ok=True)
        return project_dir

    def save(self, job: PipelineJobResponse) -> PipelineJobResponse:
        job.updated_at = datetime.now(timezone.utc)
        project_dir = Path(job.project_dir)
        project_dir.mkdir(parents=True, exist_ok=True)
        target = project_dir / "job.json"
        temporary = project_dir / "job.json.tmp"
        temporary.write_text(
            json.dumps(job.model_dump(mode="json"), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        temporary.replace(target)
        script_lines = [job.title, "", f"Chủ đề: {job.topic}", ""]
        for scene in job.scenes:
            script_lines.extend(
                [
                    f"CẢNH {scene.order}",
                    f"Lời đọc: {scene.narration}",
                    f"Prompt ảnh: {scene.image_prompt}",
                    "",
                ]
            )
        (project_dir / "kich-ban.txt").write_text(
            "\n".join(script_lines),
            encoding="utf-8",
        )
        return job

    def load(self, job_id: str) -> PipelineJobResponse:
        candidates = [
            settings.LEGACY_PROJECTS_DIR / job_id / "job.json",
            *settings.PROJECTS_DIR.glob(f"*--{job_id}/job.json"),
        ]
        target = next((candidate for candidate in candidates if candidate.exists()), None)
        if target is None:
            raise FileNotFoundError(job_id)
        return PipelineJobResponse.model_validate_json(target.read_text(encoding="utf-8"))

    def list_recent(self, limit: int = 20) -> list[PipelineJobResponse]:
        files = sorted(
            [
                *settings.PROJECTS_DIR.glob("*/job.json"),
                *settings.LEGACY_PROJECTS_DIR.glob("*/job.json"),
            ],
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        jobs: list[PipelineJobResponse] = []
        seen_ids: set[str] = set()
        for path in files:
            job = PipelineJobResponse.model_validate_json(path.read_text(encoding="utf-8"))
            if job.id in seen_ids:
                continue
            jobs.append(job)
            seen_ids.add(job.id)
            if len(jobs) >= limit:
                break
        return jobs
