"""
src/agents/xcb_nong_nghiep.py — xAI-NN: Agent Nông Nghiệp
"""
from sqlalchemy.ext.asyncio import AsyncSession
from src.agents.base_agent import BaseAgent
from src.database.models import CanBo


class XCBNongNghiep(BaseAgent):
    AGENT_ID = "xAI-NN"
    SYSTEM_PROMPT = (
        "Bạn là xAI-NN — Trợ lý AI Nông Nghiệp cho cán bộ địa phương và nông dân. "
        "Bạn hỗ trợ: chính sách hỗ trợ nông dân, vay vốn nông nghiệp, phòng trừ dịch bệnh cây trồng/vật nuôi, "
        "kỹ thuật canh tác, lịch thời vụ, xây dựng nông thôn mới, chính sách tam nông. "
        "Trả lời bằng tiếng Việt, thực tiễn, dễ áp dụng."
    )
    SKILL_PATTERNS = {
        "ho_tro_nong_dan": [
            r"ho\s*tro.*nong\s*dan",
            r"chinh\s*sach.*nong\s*nghiep",
            r"vay\s*von.*nong\s*nghiep",
            r"quy\s*tin\s*dung",
        ],
        "dich_benh": [
            r"dich\s*benh",
            r"sau\s*benh",
            r"xu\s*ly.*sau\s*hai",
            r"phong\s*tru",
            r"con\s*trung",
            r"nam.*cay\s*trong",
        ],
        "canh_tac": [
            r"ky\s*thuat.*trong",
            r"lich\s*thoi\s*vu",
            r"giong.*lua",
            r"bon\s*phan",
            r"tuoi\s*nuoc",
        ],
        "chan_nuoi": [
            r"chan\s*nuoi",
            r"gia\s*suc",
            r"gia\s*cam",
            r"thu\s*y",
            r"tiem\s*phong",
        ],
        "nong_thon_moi": [
            r"nong\s*thon\s*moi",
            r"tieu\s*chi.*xa",
            r"xay\s*dung.*nong\s*thon",
        ],
    }

    async def run_skill(self, skill_name: str, message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
        return await self._default_reply(message, nhan_vien)
