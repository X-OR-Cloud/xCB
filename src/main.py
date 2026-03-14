"""
src/main.py — FastAPI app entry point cho xHR
"""
import structlog
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import engine, get_db
from src.database.models import Base
from src.integrations.telegram_bot import register_webhook, verify_webhook_secret
from src.router import route_update
from src.scheduler import setup_scheduler

log = structlog.get_logger(__name__)


# ─── Lifespan ─────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown logic."""
    log.info("xHR_startup", env=settings.app_env)

    # Tạo bảng nếu chưa có (dev only — production dùng alembic)
    if settings.app_env == "development":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        log.info("db_tables_created")

    # Khởi động scheduler
    scheduler = setup_scheduler()
    scheduler.start()
    log.info("scheduler_started")

    yield  # ← App đang chạy

    # Shutdown
    scheduler.shutdown(wait=False)
    await engine.dispose()
    log.info("xHR_shutdown")


# ─── App ──────────────────────────────────────────────────────────────

app = FastAPI(
    title="xHR — AI-native HR Platform",
    description="Thinh Long Group | 5 MOLTY Agents via Telegram Bot",
    version="1.0.0",
    lifespan=lifespan,
)


# ─── Routes ───────────────────────────────────────────────────────────

@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "xHR", "env": settings.app_env}


@app.post("/webhook/telegram", status_code=status.HTTP_200_OK, tags=["Telegram"])
async def telegram_webhook(
    request: Request,
    db: AsyncSession = Depends(get_db),
    x_telegram_bot_api_secret_token: str | None = Header(default=None),
):
    """
    Nhận Telegram Update qua webhook.
    Telegram POST đến đây mỗi khi có tin nhắn mới.
    """
    # Xác minh webhook secret
    if not verify_webhook_secret(x_telegram_bot_api_secret_token):
        log.warning("invalid_webhook_secret")
        raise HTTPException(status_code=403, detail="Invalid secret token")

    update = await request.json()
    log.debug("telegram_update_received", update_id=update.get("update_id"))

    # Xử lý bất đồng bộ — Telegram cần response HTTP 200 nhanh
    await route_update(update, db)
    return {"ok": True}


@app.post("/admin/register-webhook", tags=["Admin"])
async def admin_register_webhook(webhook_url: str):
    """
    Đăng ký webhook URL với Telegram.
    Gọi thủ công sau khi deploy để thiết lập kết nối.
    Ví dụ: POST /admin/register-webhook?webhook_url=https://yourdomain.com/webhook/telegram
    """
    result = await register_webhook(webhook_url)
    return {"result": result}


@app.get("/admin/status", tags=["Admin"])
async def admin_status(db: AsyncSession = Depends(get_db)):
    """Trạng thái cơ bản của hệ thống."""
    from sqlalchemy import text
    try:
        await db.execute(text("SELECT 1"))
        db_ok = True
    except Exception:
        db_ok = False

    return {
        "db": "ok" if db_ok else "error",
        "claude_model": settings.claude_model,
        "env": settings.app_env,
    }
