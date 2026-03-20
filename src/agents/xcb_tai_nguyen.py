"""
src/agents/xcb_tai_nguyen.py — xAI-TN: Agent Tài Nguyên & Đất Đai
"""
from sqlalchemy.ext.asyncio import AsyncSession
from src.agents.base_agent import BaseAgent
from src.database.models import CanBo


class XCBTaiNguyen(BaseAgent):
    AGENT_ID = "xAI-TN"
    SYSTEM_PROMPT = (
        "Bạn là xAI-TN — Trợ lý AI Tài Nguyên và Đất Đai cho cán bộ địa phương. "
        "Bạn hỗ trợ: thủ tục cấp Giấy chứng nhận quyền sử dụng đất (sổ đỏ/sổ hồng), "
        "chuyển mục đích sử dụng đất, quy hoạch, giải phóng mặt bằng, "
        "môi trường, khai thác khoáng sản, cấp phép xây dựng. "
        "Luôn dẫn chiếu Luật Đất đai và văn bản liên quan. Trả lời bằng tiếng Việt."
    )
    SKILL_PATTERNS = {
        "cap_so_do": [
            r"so\s*do",
            r"so\s*hong",
            r"gcn.*quyen\s*su\s*dung\s*dat",
            r"cap.*giay\s*chung\s*nhan",
            r"dang\s*ky.*dat\s*dai",
        ],
        "chuyen_muc_dich": [
            r"chuyen.*muc\s*dich",
            r"dat\s*nong\s*nghiep.*tho\s*cu",
            r"xin\s*chuyen\s*dat",
        ],
        "quy_hoach": [
            r"quy\s*hoach",
            r"ke\s*hoach\s*su\s*dung\s*dat",
            r"ban\s*do\s*quy\s*hoach",
        ],
        "gpmb": [
            r"giai\s*phong\s*mat\s*bang",
            r"gpmb",
            r"thu\s*hoi\s*dat",
            r"den\s*bu\s*dat",
            r"boi\s*thuong",
        ],
        "moi_truong": [
            r"moi\s*truong",
            r"o\s*nhiem",
            r"danh\s*gia\s*tac\s*dong",
            r"cap\s*phep.*xa\s*thai",
        ],
        "cap_phep_xay_dung": [
            r"phep\s*xay\s*dung",
            r"xin\s*phep.*xay",
            r"thiet\s*ke\s*xay\s*dung",
        ],
    }

    async def run_skill(self, skill_name: str, message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
        return await self._default_reply(message, nhan_vien)
