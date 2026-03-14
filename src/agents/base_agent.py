"""
src/agents/base_agent.py — BaseAgent: lớp nền cho 5 MOLTY agents
"""
import re
from abc import ABC, abstractmethod

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import AuditLog, NhanVien
from src.integrations import claude_client
from src.integrations import telegram_bot

log = structlog.get_logger(__name__)


class BaseAgent(ABC):
    """
    Lớp nền cho tất cả MOLTY agents.

    Subclass phải định nghĩa:
    - AGENT_ID: str         — ví dụ "MOLTY-NB"
    - SYSTEM_PROMPT: str    — system prompt tiếng Việt cho agent này
    - SKILL_PATTERNS: dict  — {skill_name: [regex1, regex2, ...]}
    - SKILL_NAMES: list     — danh sách tên skills để classify_intent
    """

    AGENT_ID: str = "MOLTY-BASE"
    SYSTEM_PROMPT: str = "Bạn là trợ lý HR chuyên nghiệp của Thinh Long Group."
    SKILL_PATTERNS: dict[str, list[str]] = {}

    # ── Public entry point ─────────────────────────────────────────
    async def handle(
        self,
        message: str,
        nhan_vien: NhanVien,
        db: AsyncSession,
    ) -> str:
        """
        Xử lý tin nhắn và trả về nội dung reply.
        Luồng: Cache check → Regex matching → Claude intent classification → fallback.
        """
        log.info("agent_handle", agent=self.AGENT_ID, user_id=nhan_vien.telegram_user_id)
        user_id = nhan_vien.telegram_user_id

        # 0. Check Caching (Tiết kiệm 100% chi phí cho câu hỏi lặp lại)
        from src.integrations.redis_client import get_cached_response, set_cached_response
        cached_res = await get_cached_response(self.AGENT_ID, user_id, message)
        if cached_res:
            log.info("cache_hit", agent=self.AGENT_ID, user_id=user_id)
            return cached_res + "\n\n(⚡ Phản hồi từ bộ nhớ đệm)"

        # 1. Regex fast-path
        skill_name = self._match_regex(message)

        # 2. Claude intent fallback
        if skill_name is None:
            skill_names = list(self.SKILL_PATTERNS.keys())
            if skill_names:
                skill_name = await claude_client.classify_intent(
                    agent_name=self.AGENT_ID,
                    skills=skill_names,
                    user_message=message,
                )

        # 3. Dispatch skill
        try:
            if skill_name and skill_name != "unknown":
                reply = await self.run_skill(skill_name, message, nhan_vien, db)
            else:
                reply = await self._default_reply(message, nhan_vien)
        except Exception as exc:
            log.error("agent_skill_error", agent=self.AGENT_ID, skill=skill_name, error=str(exc))
            reply = "⚠️ Đã xảy ra lỗi khi xử lý yêu cầu. Vui lòng thử lại sau."
            await self._audit(db, nhan_vien, f"skill:{skill_name}", message, reply, success=False)
            return reply

        # 4. Save to Cache
        if reply:
            await set_cached_response(self.AGENT_ID, user_id, message, reply)

        await self._audit(db, nhan_vien, f"skill:{skill_name}", message, reply, success=True)
        return reply

    # ── Subclass implements ────────────────────────────────────────
    @abstractmethod
    async def run_skill(
        self,
        skill_name: str,
        message: str,
        nhan_vien: NhanVien,
        db: AsyncSession,
    ) -> str:
        """Dispatch đến skill handler cụ thể."""
        ...

    # ── Helpers ────────────────────────────────────────────────────
    def _match_regex(self, message: str) -> str | None:
        """So khớp message với regex patterns → trả tên skill hoặc None."""
        text = message.strip().lower()
        for skill_name, patterns in self.SKILL_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    log.debug("regex_match", skill=skill_name, pattern=pattern)
                    return skill_name
        return None

    async def _default_reply(self, message: str, nhan_vien: NhanVien) -> str:
        """Fallback: Tìm kiếm RAG trước khi gọi Claude."""
        from src.skills.rag_base import search_knowledge_base, generate_rag_answer
        
        # 1. Tìm ngữ cảnh từ văn bản (PDF, Word)
        context = await search_knowledge_base(message, nhan_vien)
        
        if context:
            log.info("rag_match_found", agent=self.AGENT_ID)
            return await generate_rag_answer(self.SYSTEM_PROMPT, message, context)

        # 2. Nếu không có ngữ cảnh, fallback về Claude thông thường
        system = self.SYSTEM_PROMPT + f"\n\nBạn đang hỗ trợ nhân viên: {nhan_vien.ho_ten} ({nhan_vien.phong_ban})."
        return await claude_client.ask_claude(system_prompt=system, user_message=message)

    async def _audit(
        self,
        db: AsyncSession,
        nhan_vien: NhanVien,
        hanh_dong: str,
        input_data: str,
        result: str,
        success: bool,
    ) -> None:
        """Ghi audit log."""
        try:
            entry = AuditLog(
                agent_id=self.AGENT_ID,
                nhan_vien_id=nhan_vien.id,
                telegram_user_id=nhan_vien.telegram_user_id,
                hanh_dong=hanh_dong,
                du_lieu_dau_vao=input_data[:2000],
                ket_qua=result[:2000],
                thanh_cong=success,
            )
            db.add(entry)
            await db.commit()
        except Exception as exc:
            log.error("audit_error", error=str(exc))
