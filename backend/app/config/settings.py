from dataclasses import dataclass
from functools import lru_cache
import os

from dotenv import load_dotenv


load_dotenv()
load_dotenv("backend/.env")


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "LiveOps Agent")
    app_env: str = os.getenv("APP_ENV", "development")
    api_prefix: str = os.getenv("API_PREFIX", "/api")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
    embedding_device: str | None = os.getenv("EMBEDDING_DEVICE")
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2:///liveops",
    )
    cors_origins: tuple[str, ...] = tuple(
        origin.strip()
        for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
        if origin.strip()
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
