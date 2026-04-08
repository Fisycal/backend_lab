from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    APP_NAME: str = "Backend Concepts Lab"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Backend Concepts Lab"
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    API_PREFIX: str = ""
    ALLOWED_ORIGINS: list[str] = []
    ALLOWED_HOSTS: list[str] = ["*"]

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()