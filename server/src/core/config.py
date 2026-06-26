from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

class Settings(BaseSettings):
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool = False

    model_config = SettingsConfigDict(
        env_file = Path(__file__).resolve().parents[1] / ".env",
        extra="ignore"
    )

settings = Settings()
