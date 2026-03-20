"""
src/main.py — FastAPI app entry point cho xCB Platform
"""
import structlog
from contextlib import asynccontextmanager

from fastapi import (
    Depends, FastAPI, Header, HTTPException, Request, Security, status,
    File, UploadFile, Form, BackgroundTasks
)
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import settings
from src.database import engine, get_db
from src.database.models import Base
from src.integrations.telegram_bot import register_webhook, verify_webhook_secret
from src.router import route_update
from src.scheduler import setup_scheduler
from src.api_router import router as api_router
from fastapi.middleware.cors import CORSMiddleware

# ─── Admin Security ────────────────────────────────────────────────

_admin_api_key_header = APIKeyHeader(name="X-Admin-API-Key", auto_error=False)


async def require_admin_key(api_key: str | None = Security(_admin_api_key_header)):
    """Dependency bảo vệ các endpoint /admin/*. Cần header X-Admin-API-Key."""
    if not settings.admin_api_key:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ADMIN_API_KEY chưa được cấu hình trên server.",
        )
    if api_key != settings.admin_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API key không hợp lệ.",
        )

log = structlog.get_logger(__name__)


# ─── Lifespan ─────────────────────────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup / shutdown logic."""
    log.info("xCB_startup", env=settings.app_env)

    # Tạo bảng nếu chưa có (dev only — production dùng alembic)
    if settings.app_env == "development":
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    # Khởi động scheduler
    scheduler = setup_scheduler()
    scheduler.start()
    log.info("scheduler_started")

    # Khởi tạo Qdrant
    from src.integrations.qdrant_client import init_qdrant
    await init_qdrant()
    log.info("qdrant_initialized")

    yield  # ← App đang chạy

    # Shutdown
    scheduler.shutdown(wait=False)
    await engine.dispose()
    log.info("xCB_shutdown")


# ─── App ──────────────────────────────────────────────────────────────

app = FastAPI(
    title="xCB — Nền Tảng AI Công Chức Địa Phương",
    description="xCB Platform | 9 xAI-CB Agents hỗ trợ cán bộ công chức cấp Tỉnh/Huyện/Xã",
    version="1.0.0",
    lifespan=lifespan,
)

# --- CORS ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect REST API
app.include_router(api_router)


# ─── Routes ───────────────────────────────────────────────────────────

@app.get("/health", tags=["System"])
async def health_check():
    """Health check endpoint."""
    return {"status": "ok", "service": "xCB", "version": "1.0.0", "env": settings.app_env}


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


@app.post("/admin/register-webhook", tags=["Admin"], dependencies=[Depends(require_admin_key)])
async def admin_register_webhook(webhook_url: str):
    """
    Đăng ký webhook URL với Telegram.
    Gọi thủ công sau khi deploy để thiết lập kết nối.
    Ví dụ: POST /admin/register-webhook?webhook_url=https://yourdomain.com/webhook/telegram
    """
    result = await register_webhook(webhook_url)
    return {"result": result}


_ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


@app.post("/admin/upload-document", tags=["Admin"], dependencies=[Depends(require_admin_key)])
async def admin_upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    phong_ban: str = Form("hanh_chinh"),
    description: str = Form(None)
):
    """
    Tải lên tài liệu mới (PDF/Word), lưu vào CEPH và kích hoạt xử lý OCR/RAG.
    """
    from src.integrations.xor_storage import storage
    from src.workers.document_processor import process_document
    import uuid

    # 1. Validate MIME type
    if file.content_type not in _ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Loại file không được hỗ trợ: {file.content_type}. Chỉ chấp nhận PDF và Word.",
        )

    # 2. Đọc file
    content = await file.read()
    file_ext = file.filename.split(".")[-1].lower()
    object_name = f"docs/{uuid.uuid4()}.{file_ext}"

    # 2. Upload lên CEPH
    try:
        await storage.upload_file(
            file_content=content,
            object_name=object_name,
            content_type=file.content_type
        )
    except Exception as exc:
        log.error("admin_upload_error", error=str(exc))
        raise HTTPException(status_code=500, detail=f"Lỗi upload storage: {str(exc)}")

    # 3. Kích hoạt xử lý background (OCR -> Vector)
    metadata = {
        "original_filename": file.filename,
        "phong_ban": phong_ban,
        "description": description
    }
    
    background_tasks.add_task(process_document, object_name, metadata)
    
    return {
        "status": "uploaded",
        "object_name": object_name,
        "message": "Tài liệu đang được xử lý OCR và Vectorization ngầm."
    }


@app.get("/admin/status", tags=["Admin"], dependencies=[Depends(require_admin_key)])
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
