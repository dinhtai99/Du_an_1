import json
from datetime import datetime, timezone
from pathlib import Path

from app.core.config import settings
from app.schemas.pipeline import PipelineJobResponse


class JobStore:
    def create_project_dir(self, job_id: str) -> Path:
        project_dir = settings.PROJECTS_DIR / job_id
        for name in ("images", "audio", "subtitles", "debug"):
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
        return job

    def load(self, job_id: str) -> PipelineJobResponse:
        target = settings.PROJECTS_DIR / job_id / "job.json"
        if not target.exists():
            raise FileNotFoundError(job_id)
        return PipelineJobResponse.model_validate_json(target.read_text(encoding="utf-8"))

    def list_recent(self, limit: int = 20) -> list[PipelineJobResponse]:
        files = sorted(
            settings.PROJECTS_DIR.glob("*/job.json"),
            key=lambda path: path.stat().st_mtime,
            reverse=True,
        )
        return [
            PipelineJobResponse.model_validate_json(path.read_text(encoding="utf-8"))
            for path in files[:limit]
        ]
