"""
src/agents/xcb_giao_duc.py — xAI-GD: Agent Giáo Dục
"""
from sqlalchemy.ext.asyncio import AsyncSession
from src.agents.base_agent import BaseAgent
from src.database.models import CanBo


class XCBGiaoDuc(BaseAgent):
    AGENT_ID = "xAI-GD"
    SYSTEM_PROMPT = (
        "Bạn là xAI-GD — Trợ lý AI Giáo Dục cho cán bộ công chức địa phương. "
        "Bạn hỗ trợ: chính sách tuyển sinh, học bổng, quy định trường học, phổ cập giáo dục, "
        "chính sách ưu đãi học sinh vùng khó khăn, thủ tục chuyển trường, thi cử. "
        "Trả lời bằng tiếng Việt, dễ hiểu, thực tiễn."
    )
    SKILL_PATTERNS = {
        "tuyen_sinh": [
            r"tuyen\s*sinh",
            r"dang\s*ky.*truong",
            r"nop\s*ho\s*so.*hoc",
            r"chon\s*truong",
        ],
        "hoc_bong": [
            r"hoc\s*bong",
            r"mien\s*giam.*hoc\s*phi",
            r"ho\s*tro.*hoc\s*sinh",
            r"uu\s*dai.*giao\s*duc",
        ],
        "chuyen_truong": [
            r"chuyen\s*truong",
            r"thu\s*tuc.*chuyen",
            r"ra\s*truong",
        ],
        "pho_cap_giao_duc": [
            r"pho\s*cap",
            r"xoa\s*mu\s*chu",
            r"giao\s*duc\s*bat\s*buoc",
        ],
        "chinh_sach_giao_duc": [
            r"chinh\s*sach.*giao\s*duc",
            r"quy\s*dinh.*truong\s*hoc",
            r"tieu\s*chuan.*giao\s*vien",
        ],
    }

    async def run_skill(self, skill_name: str, message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
        return await self._default_reply(message, nhan_vien)
