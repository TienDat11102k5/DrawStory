"""
DrawStory AI - Configuration Module
"""

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "DrawStory AI"
    APP_VERSION: str = "0.1.0"
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # Storage paths
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    DATA_DIR: str = os.path.join(BASE_DIR, "data")
    OUTPUTS_DIR: str = os.path.join(DATA_DIR, "outputs")
    TEMP_DIR: str = os.path.join(DATA_DIR, "temp")
    ASSETS_DIR: str = os.path.join(BASE_DIR, "assets")
    LOGS_DIR: str = os.path.join(BASE_DIR, "logs")
    LOG_FILE: str = os.path.join(LOGS_DIR, "app.log")

    # AI & Rendering
    DEFAULT_VOICE: str = "vi-VN-HoaiMyNeural"
    DEFAULT_FPS: int = 30
    DEFAULT_ASPECT_RATIO: str = "9:16"
    GEMINI_API_KEY: str = os.environ.get("GEMINI_API_KEY", "")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()

# Đảm bảo các thư mục cần thiết tồn tại
os.makedirs(settings.OUTPUTS_DIR, exist_ok=True)
os.makedirs(settings.TEMP_DIR, exist_ok=True)
os.makedirs(settings.ASSETS_DIR, exist_ok=True)
os.makedirs(settings.LOGS_DIR, exist_ok=True)
