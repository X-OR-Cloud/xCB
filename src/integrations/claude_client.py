"""
src/integrations/claude_client.py — Async AI wrapper cho xCB agents
Hỗ trợ 2 backend:
  - Anthropic (mặc định)
  - OpenAI-compatible (khi OPENAI_SOURCE=true, dùng httpx)
"""
import structlog
import httpx

from src.config import settings

log = structlog.get_logger(__name__)

# Khởi tạo Anthropic client chỉ khi cần
_anthropic_client = None

def _get_anthropic():
    global _anthropic_client
    if _anthropic_client is None:
        from anthropic import AsyncAnthropic
        _anthropic_client = AsyncAnthropic(api_key=settings.anthropic_api_key)
    return _anthropic_client


async def _ask_openai_compatible(
    system_prompt: str,
    messages: list[dict],
    max_tokens: int,
    model: str | None,
) -> str:
    """Gọi OpenAI-compatible API (X-OR Cloud / bất kỳ endpoint /chat/completions)."""
    url = f"{settings.openai_api_base.rstrip('/')}/chat/completions"
    payload = {
        "messages": [{"role": "system", "content": system_prompt}, *messages],
        "temperature": 0.2,
        "max_tokens": max_tokens,
    }
    if model:
        payload["model"] = model

    async with httpx.AsyncClient(timeout=60) as client:
        resp = await client.post(
            url,
            headers={
                "Authorization": f"Bearer {settings.openai_api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
        )
        resp.raise_for_status()
        data = resp.json()
        reply = data["choices"][0]["message"]["content"]
        log.info("openai_compat_response", model=model, url=url)
        return reply


async def _ask_anthropic(
    system_prompt: str,
    messages: list[dict],
    max_tokens: int,
    model: str,
) -> str:
    """Gọi Anthropic API với Prompt Caching."""
    client = _get_anthropic()
    system_block: dict = {"type": "text", "text": system_prompt}
    if len(system_prompt) > 1024:
        system_block["cache_control"] = {"type": "ephemeral"}

    response = await client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=0.2,
        system=[system_block],
        messages=messages,
    )
    reply = response.content[0].text
    log.info("claude_response", model=model, tokens=response.usage.output_tokens)
    return reply


async def ask_claude(
    system_prompt: str,
    user_message: str,
    history: list[dict] | None = None,
    max_tokens: int = 2048,
    model: str | None = None,
) -> str:
    """
    Gửi message tới AI backend.
    - OPENAI_SOURCE=true  → X-OR Cloud / OpenAI-compatible
    - mặc định            → Anthropic Claude
    """
    messages: list[dict] = []
    if history:
        messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    try:
        if settings.openai_source:
            selected_model = model or settings.openai_model
            return await _ask_openai_compatible(system_prompt, messages, max_tokens, selected_model)
        else:
            selected_model = model or settings.claude_model or "claude-3-5-sonnet-20241022"
            return await _ask_anthropic(system_prompt, messages, max_tokens, selected_model)
    except Exception as exc:
        log.error("ai_error", error=str(exc))
        raise


async def classify_intent(agent_name: str, skills: list[str], user_message: str) -> str:
    """
    Phân loại intent — dùng Haiku (Anthropic) hoặc OpenAI-compatible tùy config.
    """
    skill_list = "\n".join(f"- {s}" for s in skills)
    system = (
        f"Bạn là bộ phân loại intent cho {agent_name}. "
        f"Chỉ trả lời bằng ĐÚNG MỘT tên skill từ danh sách sau, không giải thích thêm:\n{skill_list}\n"
        f"Nếu không phù hợp skill nào, trả lời: unknown"
    )
    result = await ask_claude(
        system_prompt=system,
        user_message=user_message,
        max_tokens=50,
        model=None if settings.openai_source else settings.claude_haiku_model,
    )
    intent = result.strip().lower()
    if intent not in [s.lower() for s in skills] and intent != "unknown":
        return "unknown"
    return intent
