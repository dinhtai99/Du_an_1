from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class BrandSettingsUpdate(BaseModel):
    brand_name: Optional[str] = None
    logo_path: Optional[str] = None
    logo_position: Optional[str] = None # top_right, top_left, bottom_right, bottom_left
    logo_width_percent: Optional[float] = None
    logo_opacity: Optional[float] = None
    logo_margin: Optional[int] = None
    show_logo_on_outro: Optional[bool] = None
    subtitle_font: Optional[str] = None
    subtitle_font_size: Optional[int] = None
    subtitle_color: Optional[str] = None
    subtitle_stroke_color: Optional[str] = None

class BrandSettingsResponse(BaseModel):
    id: str
    brand_name: str
    logo_path: Optional[str] = None
    logo_position: str
    logo_width_percent: float
    logo_opacity: float
    logo_margin: int
    show_logo_on_outro: bool
    subtitle_font: str
    subtitle_font_size: int
    subtitle_color: str
    subtitle_stroke_color: str
    updated_at: datetime

    class Config:
        from_attributes = True

class ProviderSettingsUpdate(BaseModel):
    image_provider: Optional[str] = None # google_flow, local_image, manual_upload
    google_flow_url: Optional[str] = None
    chrome_path: Optional[str] = None
    ollama_model: Optional[str] = None
    tts_voice: Optional[str] = None
    whisper_engine: Optional[str] = None

class ProviderSettingsResponse(BaseModel):
    id: str
    image_provider: str
    google_flow_url: str
    chrome_path: str
    ollama_model: str
    tts_voice: str
    whisper_engine: str
    updated_at: datetime

    class Config:
        from_attributes = True
