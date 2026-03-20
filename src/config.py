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
    claude_model: str = "claude-3-5-sonnet-20241022"
    claude_haiku_model: str = "claude-3-haiku-20240307"

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

    # X-OR Storage (CEPH)
    xor_access_key: str | None = None
    xor_secret_key: str | None = None
    xor_endpoint_url: str = "https://s3.x-or.cloud"
    xor_bucket_name: str = "xhr-docs"

    # Qdrant
    qdrant_url: str = "http://qdrant:6333"
    qdrant_api_key: str | None = None

    # Qwen Inference
    qwen_api_base: str | None = None
    qwen_api_key: str | None = None
    qwen_vl_model: str = "Qwen/Qwen2.5-VL-72B-Instruct"
    qwen_embed_model: str = "Qwen/Qwen3-Embedding-8B"

    # Redis (Caching)
    redis_url: str = "redis://redis:6379/0"

    # OpenAI-compatible source (X-OR Cloud hoặc bất kỳ OpenAI-compatible API)
    openai_source: bool = False
    openai_api_base: str | None = None
    openai_api_key: str | None = None
    openai_model: str | None = None

    # Security
    admin_api_key: str | None = None  # Bắt buộc set trong production
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]


settings = Settings()
