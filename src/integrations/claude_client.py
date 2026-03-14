"""
src/integrations/claude_client.py — Async Claude wrapper cho xHR agents
"""
import structlog
from anthropic import AsyncAnthropic

from src.config import settings

log = structlog.get_logger(__name__)

_client = AsyncAnthropic(api_key=settings.anthropic_api_key)


async def ask_claude(
    system_prompt: str,
    user_message: str,
    history: list[dict] | None = None,
    max_tokens: int = 2048,
) -> str:
    """
    Gửi message tới Claude và nhận phản hồi dạng string.

    Args:
        system_prompt: System prompt của agent (tiếng Việt).
        user_message: Tin nhắn người dùng.
        history: Lịch sử hội thoại [{"role": "user"|"assistant", "content": "..."}]
        max_tokens: Giới hạn token phản hồi.

    Returns:
        Nội dung phản hồi từ Claude.
    """
    messages: list[dict] = []
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    try:
        response = await _client.messages.create(
            model=settings.claude_model,
            max_tokens=max_tokens,
            temperature=0.2,
            system=system_prompt,
            messages=messages,
        )
        reply = response.content[0].text
        log.info("claude_response", model=settings.claude_model, tokens_used=response.usage.output_tokens)
        return reply
    except Exception as exc:
        log.error("claude_error", error=str(exc))
        raise


async def classify_intent(agent_name: str, skills: list[str], user_message: str) -> str:
    """
    Dùng Claude để phân loại intent → trả về tên skill phù hợp nhất.

    Args:
        agent_name: Tên agent (ví dụ: MOLTY-NB).
        skills: Danh sách tên skills mà agent hỗ trợ.
        user_message: Tin nhắn người dùng cần phân loại.

    Returns:
        Tên skill (phải nằm trong danh sách skills), hoặc "unknown".
    """
    skill_list = "\n".join(f"- {s}" for s in skills)
    system = (
        f"Bạn là bộ phân loại intent cho {agent_name}. "
        f"Chỉ trả lời bằng ĐÚNG MỘT tên skill từ danh sách sau, không giải thích thêm:\n{skill_list}\n"
        f"Nếu không phù hợp skill nào, trả lời: unknown"
    )
    result = await ask_claude(system_prompt=system, user_message=user_message, max_tokens=50)
    intent = result.strip().lower()
    if intent not in [s.lower() for s in skills] and intent != "unknown":
        return "unknown"
    return intent
