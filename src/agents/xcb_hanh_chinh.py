"""
src/agents/xcb_hanh_chinh.py — xAI-HC: Agent Hành Chính Công
"""
from sqlalchemy.ext.asyncio import AsyncSession
from src.agents.base_agent import BaseAgent
from src.database.models import CanBo


class XCBHanhChinh(BaseAgent):
    AGENT_ID = "xAI-HC"
    SYSTEM_PROMPT = (
        "Bạn là xAI-HC — Trợ lý AI Hành Chính Công cho cán bộ cơ quan hành chính địa phương. "
        "Bạn hỗ trợ: hướng dẫn thủ tục hành chính (TTHC), tra cứu quy trình xử lý hồ sơ, "
        "tư vấn biểu mẫu đúng quy định, thông báo tiến độ hồ sơ, lịch tiếp dân, "
        "cơ chế một cửa, một cửa liên thông. "
        "Luôn đề xuất thời gian xử lý và hồ sơ cần thiết. Trả lời bằng tiếng Việt."
    )
    SKILL_PATTERNS = {
        "tra_cuu_thu_tuc": [
            r"thu\s*tuc",
            r"ho\s*so\s*can",
            r"dieu\s*kien.*thu\s*tuc",
            r"quy\s*trinh",
        ],
        "huong_dan_ho_so": [
            r"can\s*nhung\s*gi",
            r"bieu\s*mau",
            r"giay\s*to\s*can",
            r"huong\s*dan.*nop",
        ],
        "trang_thai_ho_so": [
            r"trang\s*thai.*ho\s*so",
            r"ho\s*so.*den\s*dau",
            r"ket\s*qua.*ho\s*so",
            r"bao\s*gio.*xong",
        ],
        "lich_tiep_dan": [
            r"lich\s*tiep\s*dan",
            r"tiep\s*cong\s*dan",
            r"gap.*can\s*bo",
            r"gio\s*lam\s*viec",
        ],
        "mot_cua": [
            r"mot\s*cua",
            r"bo\s*phan\s*tiep\s*nhan",
            r"trung\s*tam\s*hanh\s*chinh",
            r"dich\s*vu\s*cong",
        ],
    }

    async def run_skill(self, skill_name: str, message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
        return await self._default_reply(message, nhan_vien)
