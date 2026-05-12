"""
config.py
Loads environment variables from .env into a typed `settings` object.
Import `settings` from here anywhere you need config values.
"""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    database_url: str = Field(..., description = "SQLAlchemy DB URL")
    sql_echo: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

settings = Settings()