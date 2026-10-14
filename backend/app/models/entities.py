import datetime
import uuid
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    Boolean,
    Text,
    DateTime,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import relationship
from app.database.session import Base

def generate_uuid():
    return str(uuid.uuid4())

class Project(Base):
    __tablename__ = "projects"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    title = Column(String(255), nullable=False)
    topic = Column(Text, nullable=False)
    duration_target = Column(Integer, default=60) # 30, 60, 90, 120
    storytelling_style = Column(String(100), default="Tôn kính & Truyền cảm hứng")
    target_audience = Column(String(100), default="Đại chúng, người quan tâm văn hóa tâm linh")
    voice = Column(String(50), default="vi-VN-HoaiMyNeural") # or vi-VN-NamMinhNeural
    visual_style = Column(String(100), default="Tranh sơn dầu cổ điển / Thủy mặc truyền thống Việt Nam")
    product_id = Column(String(36), ForeignKey("products.id"), nullable=True)
    status = Column(String(50), default="draft") # draft, scripting, generating_images, voiceover, rendering, completed, failed
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    script = relationship("Script", back_populates="project", uselist=False, cascade="all, delete-orphan")
    jobs = relationship("GenerationJob", back_populates="project", cascade="all, delete-orphan")
    exports = relationship("VideoExport", back_populates="project", cascade="all, delete-orphan")
    product = relationship("Product", back_populates="projects")

class Script(Base):
    __tablename__ = "scripts"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False, unique=True)
    title = Column(String(255), nullable=False)
    hook = Column(Text, nullable=False)
    narration_full = Column(Text, nullable=True)
    cta_text = Column(Text, nullable=True)
    estimated_duration = Column(Float, default=60.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="script")
    scenes = relationship("Scene", back_populates="script", cascade="all, delete-orphan", order_by="Scene.order")

class Scene(Base):
    __tablename__ = "scenes"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    script_id = Column(String(36), ForeignKey("scripts.id"), nullable=False)
    order = Column(Integer, nullable=False)
    narration = Column(Text, nullable=False)
    image_prompt = Column(Text, nullable=False)
    negative_prompt = Column(Text, default="modern cars, western buildings, distorted hands, bad anatomy, text, watermark")
    duration = Column(Float, default=6.0)
    visual_style = Column(String(100), default="Tranh dân gian, sơn mài, cổ kính Việt Nam")
    transition = Column(String(50), default="fade") # fade, crossfade, zoom_in, zoom_out, pan_left, pan_right
    status = Column(String(50), default="pending") # pending, generating, completed, failed
    output_asset_path = Column(String(500), nullable=True)
    audio_asset_path = Column(String(500), nullable=True)
    subtitle_asset_path = Column(String(500), nullable=True)
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    script = relationship("Script", back_populates="scenes")
    assets = relationship("Asset", back_populates="scene", cascade="all, delete-orphan")

class Asset(Base):
    __tablename__ = "assets"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    scene_id = Column(String(36), ForeignKey("scenes.id"), nullable=True)
    asset_type = Column(String(50), nullable=False) # image, audio, subtitle, video_clip, logo, product_image
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, default=0)
    mime_type = Column(String(100), nullable=True)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    scene = relationship("Scene", back_populates="assets")

class GenerationJob(Base):
    __tablename__ = "generation_jobs"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    job_type = Column(String(50), default="full_pipeline") # full_pipeline, script_only, images_only, render_only
    status = Column(String(50), default="pending") # pending, running, waiting_for_user, paused, failed, completed, cancelled
    progress_percent = Column(Float, default=0.0)
    current_step = Column(String(100), default="initialized")
    current_scene_order = Column(Integer, default=0)
    total_scenes = Column(Integer, default=0)
    credit_budget = Column(Integer, default=50)
    credits_used = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    requires_user_action = Column(Boolean, default=False)
    user_action_prompt = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="jobs")
    events = relationship("JobEvent", back_populates="job", cascade="all, delete-orphan", order_by="JobEvent.created_at.desc()")

class JobEvent(Base):
    __tablename__ = "job_events"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    job_id = Column(String(36), ForeignKey("generation_jobs.id"), nullable=False)
    event_type = Column(String(50), nullable=False) # info, warning, error, pause, resume, progress
    message = Column(Text, nullable=False)
    details_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    job = relationship("GenerationJob", back_populates="events")

class Product(Base):
    __tablename__ = "products"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    promo_image_path = Column(String(500), nullable=True)
    logo_path = Column(String(500), nullable=True)
    website = Column(String(255), nullable=True)
    cta_text = Column(String(255), default="Liên hệ ngay để nhận ưu đãi phần mềm & máy in sớ")
    intro_text = Column(Text, nullable=True)
    duration_seconds = Column(Float, default=6.0)
    is_default = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    projects = relationship("Project", back_populates="product")

class BrandSettings(Base):
    __tablename__ = "brand_settings"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    brand_name = Column(String(255), default="VietCulture Studio")
    logo_path = Column(String(500), nullable=True)
    logo_position = Column(String(50), default="top_right") # top_right, top_left, bottom_right, bottom_left
    logo_width_percent = Column(Float, default=16.0)
    logo_opacity = Column(Float, default=0.88)
    logo_margin = Column(Integer, default=40)
    show_logo_on_outro = Column(Boolean, default=True)
    subtitle_font = Column(String(100), default="Arial")
    subtitle_font_size = Column(Integer, default=24)
    subtitle_color = Column(String(50), default="&H00FFFFFF")
    subtitle_stroke_color = Column(String(50), default="&H00000000")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class ProviderSettings(Base):
    __tablename__ = "provider_settings"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    image_provider = Column(String(50), default="google_flow") # google_flow, local_image, manual_upload
    google_flow_url = Column(String(255), default="https://flow.google.com")
    chrome_path = Column(String(500), default="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
    ollama_model = Column(String(100), default="qwen2.5:3b")
    tts_voice = Column(String(100), default="vi-VN-HoaiMyNeural")
    whisper_engine = Column(String(50), default="submaker") # submaker, whisper_cli
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

class VideoExport(Base):
    __tablename__ = "video_exports"

    id = Column(String(36), primary_key=True, default=generate_uuid)
    project_id = Column(String(36), ForeignKey("projects.id"), nullable=False)
    video_path = Column(String(500), nullable=False)
    resolution = Column(String(50), default="1080x1920")
    fps = Column(Integer, default=30)
    duration = Column(Float, default=0.0)
    file_size_bytes = Column(Integer, default=0)
    status = Column(String(50), default="ready")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    project = relationship("Project", back_populates="exports")
