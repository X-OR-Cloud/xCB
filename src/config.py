"""
src/config.py — Cấu hình ứng dụng xHR từ biến môi trường (.env)
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Database
    database_url: str
    database_sync_url: str

    # Claude / Anthropic
    anthropic_api_key: str
    claude_model: str = "claude-opus-4-6"

    # Telegram
    telegram_bot_token: str
    telegram_webhook_secret: str
    
    # Email / SMTP
    smtp_server: str = "smtp.gmail.com"
    smtp_port: int = 587
    smtp_username: str | None = None
    smtp_password: str | None = None
    email_from: str = "xhr-noreply@thinhlonggroup.com"

    # App
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000


settings = Settings()
