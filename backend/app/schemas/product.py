from typing import Optional
from datetime import datetime
from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    promo_image_path: Optional[str] = None
    logo_path: Optional[str] = None
    website: Optional[str] = None
    cta_text: str = "Liên hệ ngay để nhận ưu đãi phần mềm & máy in sớ"
    intro_text: Optional[str] = None
    duration_seconds: float = 6.0
    is_default: bool = False

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    promo_image_path: Optional[str] = None
    logo_path: Optional[str] = None
    website: Optional[str] = None
    cta_text: Optional[str] = None
    intro_text: Optional[str] = None
    duration_seconds: Optional[float] = None
    is_default: Optional[bool] = None

class ProductResponse(ProductBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
