import os
from pathlib import Path
from pydantic_settings import BaseSettings

# Get the project root directory
ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Personal Drive"
    
    # Storage configuration
    # For local development:
    # STORAGE_DIR: str = os.path.join(ROOT_DIR, "storage")
    
    # For external hard drive (uncomment and modify this line when ready):
    STORAGE_DIR: str = "/Volumes/Personal Use/personal_drive_storage"
    
    MAX_UPLOAD_SIZE: int = 1024 * 1024 * 1024  # 1GB max file size
    
    # Database
    DATABASE_URL: str = f"sqlite:///{ROOT_DIR}/personal_drive.db"
    
    # CORS
    BACKEND_CORS_ORIGINS: list[str] = ["*"]
    
    class Config:
        case_sensitive = True


settings = Settings()

# Ensure storage directory exists
os.makedirs(settings.STORAGE_DIR, exist_ok=True)
