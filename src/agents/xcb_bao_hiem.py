"""
src/agents/xcb_bao_hiem.py — xAI-BH: Agent Bảo Hiểm Xã Hội
"""
from sqlalchemy.ext.asyncio import AsyncSession
from src.agents.base_agent import BaseAgent
from src.database.models import CanBo


class XCBBaoHiem(BaseAgent):
    AGENT_ID = "xAI-BH"
    SYSTEM_PROMPT = (
        "Bạn là xAI-BH — Trợ lý AI Bảo Hiểm Xã Hội cho cán bộ cơ quan BHXH địa phương. "
        "Bạn hỗ trợ: các chế độ BHXH (ốm đau, thai sản, tai nạn lao động, hưu trí, tử tuất), "
        "BHYT, BHTN, thủ tục giải quyết chế độ, tra cứu quy định, hướng dẫn biểu mẫu. "
        "Trả lời bằng tiếng Việt, dẫn chiếu điều khoản Luật BHXH cụ thể."
    )
    SKILL_PARAMS = {}
    SKILL_PATTERNS = {
        "bhxh_mot_lan": [
            r"mot\s*lan",
            r"rut\s*bhxh",
            r"huong\s*bhxh\s*mot\s*lan",
        ],
        "che_do_thai_san": [
            r"thai\s*san",
            r"nghi\s*sinh",
            r"che\s*do.*sinh\s*con",
            r"tre\s*so\s*sinh",
        ],
        "huu_tri": [
            r"huu\s*tri",
            r"nghi\s*huu",
            r"luong\s*huu",
            r"du\s*dieu\s*kien.*huu",
        ],
        "bhyt": [
            r"bhyt",
            r"bao\s*hiem\s*y\s*te",
            r"the\s*bhyt",
            r"kham\s*chua\s*benh",
        ],
        "that_nghiep": [
            r"that\s*nghiep",
            r"bhtn",
            r"tro\s*cap.*that\s*nghiep",
            r"mat\s*viec",
        ],
        "tai_nan_lao_dong": [
            r"tai\s*nan\s*lao\s*dong",
            r"benh\s*nghe\s*nghiep",
            r"mat\s*suc\s*lao\s*dong",
        ],
    }

    async def run_skill(self, skill_name: str, message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
        return await self._default_reply(message, nhan_vien)
