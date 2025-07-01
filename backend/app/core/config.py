import os
from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Python Web Application Demo"
    ENVIRONMENT: str = "dev"
    DATABASE_URL: str = "sqlite:///./app.db"
    SECRET_KEY: str = "test_secret_key"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_DAYS: int = 30

    LOG_LEVEL: str = "INFO"
    DEBUG: bool = False
    ALLOWED_ORIGINS: str = "http://localhost:8000"
    TEST_DATABASE_URL: str = "sqlite:///./test.db"

    class Config:
        env_file = os.path.join(str(Path(__file__).parent.parent.parent), ".env")
        case_sensitive = True  # Enforce exact case matching
        env_file_encoding = "utf-8"


if not os.path.exists(Settings.Config.env_file):
    import warnings

    warnings.warn(
        f".env file not found at {Settings.Config.env_file}. Using default settings."
    )

settings = Settings()
