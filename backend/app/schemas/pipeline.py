from datetime import datetime, timezone
from typing import Literal, Optional

from pydantic import BaseModel, Field


class PipelineSceneInput(BaseModel):
    narration: str
    image_prompt: Optional[str] = None
    image_path: Optional[str] = None


class PipelineStartRequest(BaseModel):
    topic: str = Field(min_length=3, max_length=500)
    title: Optional[str] = None
    duration_target: int = Field(default=60, ge=15, le=300)
    scene_count: int = Field(default=10, ge=3, le=24)
    storytelling_style: str = "Tôn kính và truyền cảm hứng"
    visual_style: str = "Tranh sơn mài và thủy mặc truyền thống Việt Nam"
    voice: str = "vi-VN-HoaiMyNeural"
    product_name: str = "Phần mềm viết sớ và máy in sớ Việt Nam"
    cta_text: str = "Liên hệ để được tư vấn phần mềm viết sớ và máy in sớ."
    extra_context: Optional[str] = None
    logo_path: Optional[str] = None
    scenes: list[PipelineSceneInput] = Field(default_factory=list)
    generate_images: bool = True
    render_video: bool = True


class PipelineSceneState(BaseModel):
    order: int
    narration: str
    image_prompt: str
    status: Literal["pending", "generating", "completed", "failed"] = "pending"
    image_path: Optional[str] = None
    audio_path: Optional[str] = None
    subtitle_path: Optional[str] = None
    error_message: Optional[str] = None


class PipelineJobResponse(BaseModel):
    id: str
    title: str
    topic: str
    status: Literal[
        "pending", "running", "waiting_for_user", "failed", "completed"
    ] = "pending"
    progress_percent: float = 0
    current_step: str = "Khởi tạo"
    user_action_prompt: Optional[str] = None
    error_message: Optional[str] = None
    output_video_path: Optional[str] = None
    output_video_url: Optional[str] = None
    project_dir: str
    request: PipelineStartRequest
    scenes: list[PipelineSceneState] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class FlowSessionStatus(BaseModel):
    open: bool
    ready: bool
    url: Optional[str] = None
    message: str
