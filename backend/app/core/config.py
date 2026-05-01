"""
Application configuration.
"""
from pydantic import BaseSettings, PostgresDsn, RedisDsn, AnyHttpUrl
from typing import List, Optional
from pydantic.networks import AnyUrl

class Settings(BaseSettings):
    # Project
    PROJECT_NAME: str = "AI SDLC Orchestrator"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"

    # Database
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_DB: str = "ai_sdlc"
    DATABASE_URL: Optional[PostgresDsn] = None

    # Redis
    REDIS_URL: Optional[RedisDsn] = None

    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # LLM Configuration
    LLM_PROVIDER: str = "mock"  # mock, openai, huggingface
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    HF_ENDPOINT_URL: Optional[AnyHttpUrl] = None
    HF_API_KEY: Optional[str] = None

    # CORS
    BACKEND_CORS_ORIGINS: List[AnyUrl] = [
        "http://localhost:3000",
        "http://localhost:8000",
    ]

    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()