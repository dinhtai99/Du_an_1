import asyncio
import shutil
import tempfile
from pathlib import Path

from app.core.config import settings
from app.schemas.pipeline import PipelineSceneState


class VideoRenderError(RuntimeError):
    pass


class VideoRenderer:
    async def render(
        self,
        scenes: list[PipelineSceneState],
        output_path: Path,
        logo_path: str | None = None,
    ) -> Path:
        valid_scenes = [
            scene
            for scene in scenes
            if scene.image_path and scene.audio_path and scene.subtitle_path
        ]
        if len(valid_scenes) != len(scenes):
            raise VideoRenderError("Một số cảnh còn thiếu ảnh, âm thanh hoặc phụ đề.")

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix="vietculture-render-") as temp_name:
            temp_dir = Path(temp_name)
            clips: list[Path] = []
            for scene in valid_scenes:
                clip_path = temp_dir / f"scene_{scene.order:03d}.mp4"
                local_subtitle = temp_dir / f"scene_{scene.order:03d}.srt"
                shutil.copy2(scene.subtitle_path, local_subtitle)
                await self._render_scene(
                    scene=scene,
                    subtitle_path=local_subtitle,
                    output_path=clip_path,
                    logo_path=logo_path,
                )
                clips.append(clip_path)

            concat_file = temp_dir / "clips.txt"
            concat_file.write_text(
                "".join(f"file '{clip.name}'\n" for clip in clips),
                encoding="utf-8",
            )
            await self._run(
                [
                    settings.FFMPEG_PATH,
                    "-y",
                    "-f",
                    "concat",
                    "-safe",
                    "0",
                    "-i",
                    str(concat_file),
                    "-c",
                    "copy",
                    "-movflags",
                    "+faststart",
                    str(output_path),
                ],
                cwd=temp_dir,
            )
        return output_path

    async def _render_scene(
        self,
        scene: PipelineSceneState,
        subtitle_path: Path,
        output_path: Path,
        logo_path: str | None,
    ) -> None:
        duration = await self._audio_duration(Path(scene.audio_path)) + 0.35
        video_filter = (
            f"scale={settings.VIDEO_WIDTH}:{settings.VIDEO_HEIGHT}:"
            "force_original_aspect_ratio=increase,"
            f"crop={settings.VIDEO_WIDTH}:{settings.VIDEO_HEIGHT},setsar=1,"
            f"subtitles='{subtitle_path}':force_style='FontName=Arial,FontSize=22,"
            "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,"
            "Outline=2,Shadow=1,Alignment=2,MarginV=110'"
        )
        command = [
            settings.FFMPEG_PATH,
            "-y",
            "-loop",
            "1",
            "-framerate",
            str(settings.VIDEO_FPS),
            "-i",
            str(scene.image_path),
            "-i",
            str(scene.audio_path),
        ]
        logo = Path(logo_path).expanduser() if logo_path else None
        if logo and logo.is_file():
            command.extend(["-loop", "1", "-i", str(logo)])
            command.extend(
                [
                    "-filter_complex",
                    f"[0:v]{video_filter}[base];[2:v]scale=180:-1[logo];"
                    "[base][logo]overlay=W-w-40:40[outv]",
                    "-map",
                    "[outv]",
                    "-map",
                    "1:a:0",
                ]
            )
        else:
            command.extend(["-vf", video_filter, "-map", "0:v:0", "-map", "1:a:0"])

        command.extend(
            [
                "-t",
                f"{duration:.3f}",
                "-c:v",
                settings.VIDEO_ENCODER,
            ]
        )
        if settings.VIDEO_ENCODER.endswith("videotoolbox"):
            command.extend(["-allow_sw", "1"])
        command.extend(
            [
                "-b:v",
                settings.VIDEO_BITRATE,
                "-pix_fmt",
                "yuv420p",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-ar",
                "48000",
                "-shortest",
                str(output_path),
            ]
        )
        try:
            await self._run(command)
        except VideoRenderError:
            if not settings.VIDEO_ENCODER.endswith("videotoolbox"):
                raise
            fallback = command.copy()
            encoder_index = fallback.index(settings.VIDEO_ENCODER)
            fallback[encoder_index] = "libx264"
            allow_sw_index = fallback.index("-allow_sw")
            del fallback[allow_sw_index : allow_sw_index + 2]
            await self._run(fallback)

    async def _audio_duration(self, audio_path: Path) -> float:
        ffprobe = str(Path(settings.FFMPEG_PATH).with_name("ffprobe"))
        process = await asyncio.create_subprocess_exec(
            ffprobe,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(audio_path),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise VideoRenderError(stderr.decode(errors="replace").strip())
        return float(stdout.decode().strip())

    async def _run(self, command: list[str], cwd: Path | None = None) -> None:
        process = await asyncio.create_subprocess_exec(
            *command,
            cwd=str(cwd) if cwd else None,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )
        _, stderr = await process.communicate()
        if process.returncode != 0:
            message = stderr.decode(errors="replace")[-4000:]
            raise VideoRenderError(message.strip())
