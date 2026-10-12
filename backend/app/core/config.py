"""
app/core/config.py
------------------
Application configuration via pydantic-settings.
All values are loaded from environment variables or a .env file.
"""

from __future__ import annotations

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration object.

    Values are resolved in this order (highest priority first):
    1. Real environment variables
    2. Variables in the .env file
    3. Field defaults declared below
    """

    # ── Application ──────────────────────────────────────────────────────────
    APP_ENV: str = "development"
    APP_DEBUG: bool = False
    SECRET_KEY: str = "change-this-secret"

    # ── Firebase / Firestore ─────────────────────────────────────────────────
    # Path to the service account JSON file (never commit this file).
    # Set FIREBASE_CREDENTIALS_PATH in your .env to an absolute path or a
    # path relative to the directory you launch uvicorn from.
    FIREBASE_CREDENTIALS_PATH: str = "firebase-credentials.json"

    # ── CORS ─────────────────────────────────────────────────────────────────
    CORS_ORIGINS: list[str] = ["http://localhost:8000", "http://127.0.0.1:8000"]

    # ── Rate limiting ─────────────────────────────────────────────────────────
    RATE_LIMIT_ENQUIRIES: str = "5/minute"

    # ── pydantic-settings config ──────────────────────────────────────────────
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # ── Validators ────────────────────────────────────────────────────────────
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def _parse_cors(cls, value: str | list[str]) -> list[str]:
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        return value


# Module-level singleton — import this everywhere.
settings = Settings()
