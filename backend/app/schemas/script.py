from typing import List, Optional
from pydantic import BaseModel, Field

class SceneBase(BaseModel):
    order: int
    narration: str = Field(..., description="Lời thuyết minh truyền cảm, đúng chuẩn văn hóa")
    image_prompt: str = Field(..., description="Prompt tiếng Anh chi tiết để tạo ảnh văn hóa Việt Nam chất lượng cao")
    negative_prompt: Optional[str] = Field(
        default="modern elements, deformed anatomy, extra limbs, ugly, text, watermark, bad calligraphy",
        description="Negative prompt"
    )
    duration: float = Field(default=6.0, description="Thời lượng cảnh tính bằng giây")
    visual_style: Optional[str] = Field(default="Vietnamese traditional folk art, classic lacquer, sacred ambiance")
    transition: Optional[str] = Field(default="zoom_in", description="zoom_in, zoom_out, pan_left, pan_right, crossfade, fade")

class SceneCreate(SceneBase):
    pass

class SceneUpdate(BaseModel):
    narration: Optional[str] = None
    image_prompt: Optional[str] = None
    negative_prompt: Optional[str] = None
    duration: Optional[float] = None
    visual_style: Optional[str] = None
    transition: Optional[str] = None
    status: Optional[str] = None

class SceneResponse(SceneBase):
    id: str
    script_id: str
    status: str
    output_asset_path: Optional[str] = None
    audio_asset_path: Optional[str] = None
    subtitle_asset_path: Optional[str] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True

class ScriptGenerateRequest(BaseModel):
    topic: str = Field(..., description="Chủ đề video, ví dụ: 'Sớ Táo Quân là gì? Vì sao người Việt có tục dâng sớ?'")
    duration_target: int = Field(default=60, description="30, 60, 90 hoặc 120 giây")
    storytelling_style: str = Field(default="Tôn kính & Truyền cảm hứng")
    target_audience: str = Field(default="Đại chúng, người quan tâm phong tục & nghi lễ truyền thống")
    voice: str = Field(default="vi-VN-HoaiMyNeural") # vi-VN-NamMinhNeural
    visual_style: str = Field(default="Tranh thủy mặc & Tranh dân gian cổ truyền Việt Nam, trang nghiêm ấm cúng")
    product_name: Optional[str] = Field(default="Phần mềm viết sớ & Máy in sớ Việt Nam")
    extra_context: Optional[str] = Field(default=None, description="Kiến thức bổ sung hoặc trích đoạn tài liệu nghiên cứu")

class StructuredScriptOutput(BaseModel):
    title: str = Field(..., description="Tiêu đề video giật tít, chuẩn SEO TikTok/Shorts")
    hook: str = Field(..., description="Câu mở đầu thu hút trong 3-5 giây đầu tiên")
    scenes: List[SceneBase] = Field(..., description="Danh sách 5 đến 10 cảnh chi tiết")
    cta_text: str = Field(..., description="Lời kêu gọi hành động quảng bá sản phẩm ở cuối video")

class ScriptResponse(BaseModel):
    id: str
    project_id: str
    title: str
    hook: str
    narration_full: Optional[str] = None
    cta_text: Optional[str] = None
    estimated_duration: float
    scenes: List[SceneResponse] = []

    class Config:
        from_attributes = True
