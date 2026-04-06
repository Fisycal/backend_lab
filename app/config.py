from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from typing import List


class Settings(BaseSettings):
    # --- App Info ---
    APP_NAME: str = "backend_lab"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # --- API ---
    API_PREFIX: str = "/api"

    # --- Security ---
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # --- Database ---
    DATABASE_URL: str

    # --- CORS ---
    ALLOWED_ORIGINS: List[str] = []

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # prevents crash if extra env vars exist
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()