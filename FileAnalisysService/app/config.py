from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    database_url: str = Field(..., env="DATABASE_URL")
    storage_path: str = Field(..., env="STORAGE_PATH")
    remote_storage_url: str = Field(..., env="REMOTE_STORAGE_URL")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()