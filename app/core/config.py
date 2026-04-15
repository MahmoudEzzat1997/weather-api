from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings


BASE_DIR = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    weather_api_key: str | None = None
    weather_base_url: str = "http://api.weatherstack.com"

    model_config = {
        "env_file": BASE_DIR / ".env",
        "env_file_encoding": "utf-8",
    }




@lru_cache
def get_settings() -> Settings:
    return Settings()
