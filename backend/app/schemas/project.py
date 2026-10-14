from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field
from app.schemas.script import ScriptResponse, ScriptGenerateRequest

class ProjectCreate(BaseModel):
    title: Optional[str] = None
    topic: str
    duration_target: int = 60
    storytelling_style: str = "Tôn kính & Truyền cảm hứng"
    target_audience: str = "Đại chúng, người quan tâm văn hóa tâm linh"
    voice: str = "vi-VN-HoaiMyNeural"
    visual_style: str = "Tranh sơn dầu cổ điển / Thủy mặc truyền thống Việt Nam"
    product_id: Optional[str] = None

class ProjectUpdate(BaseModel):
    title: Optional[str] = None
    topic: Optional[str] = None
    duration_target: Optional[int] = None
    storytelling_style: Optional[str] = None
    target_audience: Optional[str] = None
    voice: Optional[str] = None
    visual_style: Optional[str] = None
    product_id: Optional[str] = None
    status: Optional[str] = None

class VideoExportResponse(BaseModel):
    id: str
    video_path: str
    resolution: str
    fps: int
    duration: float
    file_size_bytes: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class ProjectResponse(BaseModel):
    id: str
    title: str
    topic: str
    duration_target: int
    storytelling_style: str
    target_audience: str
    voice: str
    visual_style: str
    product_id: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    script: Optional[ScriptResponse] = None
    exports: List[VideoExportResponse] = []

    class Config:
        from_attributes = True
