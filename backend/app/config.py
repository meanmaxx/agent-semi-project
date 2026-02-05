"""Application configuration."""

import os
from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # vLLM Configuration
    vllm_base_url: str = "http://localhost:8000"
    vllm_model: str = "Qwen/Qwen2.5-7B-Instruct"
    tool_call_parser: str = "hermes"

    # Backend Configuration
    backend_port: int = 8080
    allowed_origins: str = "http://localhost:5173,http://localhost:3000"
    log_level: str = "info"

    # Database
    database_url: str = "sqlite:///./budget.db"

    # Debug
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
