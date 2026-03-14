"""
src/integrations/telegram_bot.py — Telegram Bot API wrapper cho xHR
"""
import structlog
import httpx

from src.config import settings

log = structlog.get_logger(__name__)

TELEGRAM_API_BASE = f"https://api.telegram.org/bot{settings.telegram_bot_token}"


async def send_message(
    chat_id: int | str,
    text: str,
    parse_mode: str = "Markdown",
    reply_markup: dict | None = None,
) -> dict:
    """
    Gửi tin nhắn văn bản qua Telegram Bot API.

    Args:
        chat_id: ID của chat (user hoặc group).
        text: Nội dung tin nhắn (hỗ trợ Markdown/HTML).
        parse_mode: "Markdown" | "HTML" | None.
        reply_markup: InlineKeyboard hoặc ReplyKeyboard (dict).

    Returns:
        JSON response từ Telegram API.
    """
    payload: dict = {"chat_id": chat_id, "text": text}
    if parse_mode:
        payload["parse_mode"] = parse_mode
    if reply_markup:
        payload["reply_markup"] = reply_markup

    async with httpx.AsyncClient(timeout=10.0) as client:
        try:
            resp = await client.post(f"{TELEGRAM_API_BASE}/sendMessage", json=payload)
            resp.raise_for_status()
            log.info("telegram_sent", chat_id=chat_id, chars=len(text))
            return resp.json()
        except httpx.HTTPStatusError as exc:
            log.error("telegram_http_error", status=exc.response.status_code, body=exc.response.text)
            raise
        except Exception as exc:
            log.error("telegram_send_error", error=str(exc))
            raise


async def send_typing_action(chat_id: int | str) -> None:
    """Hiển thị 'typing...' indicator để cải thiện UX."""
    payload = {"chat_id": chat_id, "action": "typing"}
    async with httpx.AsyncClient(timeout=5.0) as client:
        try:
            await client.post(f"{TELEGRAM_API_BASE}/sendChatAction", json=payload)
        except Exception:
            pass  # Non-critical


def verify_webhook_secret(secret_token_header: str | None) -> bool:
    """
    Xác minh request từ Telegram bằng header X-Telegram-Bot-Api-Secret-Token.
    Telegram gửi secret này nếu ta đặt khi đăng ký webhook.
    """
    if not settings.telegram_webhook_secret:
        return True  # Không bật verification trong dev
    return secret_token_header == settings.telegram_webhook_secret


async def register_webhook(webhook_url: str) -> dict:
    """
    Đăng ký webhook URL với Telegram.
    Gọi một lần khi deploy / startup (production).
    """
    payload = {
        "url": webhook_url,
        "secret_token": settings.telegram_webhook_secret,
        "allowed_updates": ["message", "callback_query"],
    }
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.post(f"{TELEGRAM_API_BASE}/setWebhook", json=payload)
        resp.raise_for_status()
        result = resp.json()
        log.info("webhook_registered", url=webhook_url, result=result)
        return result
