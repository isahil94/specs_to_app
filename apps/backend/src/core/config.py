"""Application configuration."""

import os
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""

    # App
    APP_NAME: str = "Task Management API"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")

    # API
    API_HOST: str = "127.0.0.1"
    API_PORT: int = 8001
    API_PREFIX: str = "/api/v1"
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]

    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "sqlite:///./test.db"
    )
    DB_ECHO: bool = DEBUG

    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "your-secret-key-change-in-production"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_HASH_ALGORITHM: str = "bcrypt"
    PASSWORD_MIN_LENGTH: int = 8
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_NUMBERS: bool = True
    PASSWORD_REQUIRE_SPECIAL: bool = True

    # JWT
    JWT_ALGORITHM: str = "HS256"
    JWT_SECRET: str = os.getenv("JWT_SECRET", SECRET_KEY)

    # Session
    SESSION_TIMEOUT_MINUTES: int = 60
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_DURATION_MINUTES: int = 15

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"

    # Cache
    REDIS_URL: Optional[str] = os.getenv("REDIS_URL", None)
    CACHE_TTL_SECONDS: int = 300

    class Config:
        """Pydantic settings config."""

        env_file = ".env"
        case_sensitive = True


settings = Settings()
