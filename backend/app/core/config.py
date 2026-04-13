"""Application configuration settings."""

import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application Version
    PROJECT_VERSION: str = os.getenv("PROJECT_VERSION", "0.1.0")
    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./board_games.db")

    # Security
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "replace-with-a-strong-random-secret-at-least-32-chars"
    )
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

    # API
    API_V_STR: str = os.getenv("API_V_STR", "/api/v1")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Board Game Management")


settings = Settings()
