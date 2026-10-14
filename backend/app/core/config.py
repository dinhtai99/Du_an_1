from pathlib import Path
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).resolve().parent.parent.parent
STORAGE_DIR = BASE_DIR.parent / "storage"

class Settings(BaseSettings):
    PROJECT_NAME: str = "VietCulture AI Studio"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Storage directories
    STORAGE_DIR: Path = STORAGE_DIR
    PROJECTS_DIR: Path = STORAGE_DIR / "projects"
    ASSETS_DIR: Path = STORAGE_DIR / "assets"
    PRODUCTS_DIR: Path = STORAGE_DIR / "products"
    LOGOS_DIR: Path = STORAGE_DIR / "logos"
    EXPORTS_DIR: Path = STORAGE_DIR / "exports"
    KNOWLEDGE_DIR: Path = STORAGE_DIR / "knowledge"
    CHROME_PROFILE_DIR: Path = STORAGE_DIR / "flow_browser_profile"
    
    # Database
    DATABASE_URL: str = f"sqlite:///{STORAGE_DIR / 'vietculture.db'}"
    
    # AI Providers & Tooling
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:3b"
    
    # Browser & Playwright
    CHROME_EXECUTABLE_PATH: str = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
    GOOGLE_FLOW_URL: str = "https://flow.google.com"
    BROWSER_HEADLESS: bool = False
    BROWSER_TIMEOUT_MS: int = 45000
    FLOW_GENERATION_TIMEOUT_MS: int = 240000
    FLOW_REMOTE_DEBUGGING_PORT: int = 9223
    
    # Audio & Video Engine
    FFMPEG_PATH: str = "/opt/homebrew/bin/ffmpeg"
    WHISPER_PATH: str = "/opt/homebrew/bin/whisper-cli"
    DEFAULT_TTS_VOICE: str = "vi-VN-HoaiMyNeural" # vi-VN-NamMinhNeural
    DEFAULT_TTS_RATE: str = "+0%"
    DEFAULT_TTS_PITCH: str = "+0Hz"
    
    # Video Specs
    VIDEO_WIDTH: int = 1080
    VIDEO_HEIGHT: int = 1920
    VIDEO_FPS: int = 30
    VIDEO_ENCODER: str = "h264_videotoolbox"
    VIDEO_BITRATE: str = "6M"
    VIDEO_OVERLAY_PATH: Path = BASE_DIR / "assets" / "video-overlay.png"

    # Local web apps
    CORS_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"
    
    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

# Ensure directories exist
for folder in [
    settings.STORAGE_DIR,
    settings.PROJECTS_DIR,
    settings.ASSETS_DIR,
    settings.PRODUCTS_DIR,
    settings.LOGOS_DIR,
    settings.EXPORTS_DIR,
    settings.KNOWLEDGE_DIR,
    settings.CHROME_PROFILE_DIR,
]:
    folder.mkdir(parents=True, exist_ok=True)
