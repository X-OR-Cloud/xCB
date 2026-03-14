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
    model: str | None = None  # Cho phép chọn model linh hoạt
) -> str:
    """
    Gửi message tới Claude.
    Hỗ trợ Prompt Caching của Anthropic nếu system_prompt đủ dài.
    """
    messages: list[dict] = []
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    # Sử dụng Sonnet làm mặc định cho chất lượng, Haiku cho tốc độ/giá
    selected_model = model or settings.claude_model or "claude-3-5-sonnet-20241022"

    try:
        response = await _client.messages.create(
            model=selected_model,
            max_tokens=max_tokens,
            temperature=0.2,
            system=[
                {
                    "type": "text", 
                    "text": system_prompt,
                    "cache_control": {"type": "ephemeral"} if len(system_prompt) > 1024 else None
                }
            ],
            messages=messages,
        )
        reply = response.content[0].text
        log.info("claude_response", model=selected_model, tokens=response.usage.output_tokens)
        return reply
    except Exception as exc:
        log.error("claude_error", error=str(exc))
        raise

async def classify_intent(agent_name: str, skills: list[str], user_message: str) -> str:
    """
    Dùng Claude 3 Haiku để phân loại intent (Rẻ hơn 12 lần so với Sonnet).
    """
    skill_list = "\n".join(f"- {s}" for s in skills)
    system = (
        f"Bạn là bộ phân loại intent cho {agent_name}. "
        f"Chỉ trả lời bằng ĐÚNG MỘT tên skill từ danh sách sau, không giải thích thêm:\n{skill_list}\n"
        f"Nếu không phù hợp skill nào, trả lời: unknown"
    )
    # Sử dụng Haiku từ config cho task này
    result = await ask_claude(
        system_prompt=system, 
        user_message=user_message, 
        max_tokens=50,
        model=settings.claude_haiku_model
    )
    intent = result.strip().lower()
    if intent not in [s.lower() for s in skills] and intent != "unknown":
        return "unknown"
    return intent
