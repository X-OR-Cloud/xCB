"""
src/integrations/redis_client.py — Quản lý caching kết quả AI bằng Redis
"""
import redis.asyncio as redis
from src.config import settings
import structlog
import json
import hashlib

log = structlog.get_logger(__name__)

# Kết nối Redis
_redis_client = None

def get_redis():
    global _redis_client
    if _redis_client is None:
        _redis_client = redis.from_url(settings.redis_url, encoding="utf-8", decode_responses=True)
    return _redis_client

def generate_cache_key(agent_id: str, user_id: int, message: str) -> str:
    """Tạo ra một key duy nhất dựa trên nội dung câu hỏi."""
    # Chuẩn hóa tin nhắn để tránh cache hụt do khoảng trắng
    clean_msg = message.strip().lower()
    msg_hash = hashlib.md5(clean_msg.encode()).hexdigest()
    return f"xhr:cache:{agent_id}:{user_id}:{msg_hash}"

async def get_cached_response(agent_id: str, user_id: int, message: str) -> str | None:
    """Lấy câu trả lời đã lưu trong cache."""
    try:
        r = get_redis()
        key = generate_cache_key(agent_id, user_id, message)
        return await r.get(key)
    except Exception as exc:
        log.error("redis_get_error", error=str(exc))
        return None

async def set_cached_response(agent_id: str, user_id: int, message: str, response: str, expire: int = 86400):
    """
    Lưu câu trả lời vào cache.
    Mặc định lưu trong 24 giờ (86400 giây).
    """
    try:
        r = get_redis()
        key = generate_cache_key(agent_id, user_id, message)
        await r.set(key, response, ex=expire)
        log.info("response_cached", key=key)
    except Exception as exc:
        log.error("redis_set_error", error=str(exc))
