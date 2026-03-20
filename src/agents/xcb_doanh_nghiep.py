"""
src/agents/xcb_doanh_nghiep.py — xAI-DN: Agent Hỗ Trợ Doanh Nghiệp
"""
from sqlalchemy.ext.asyncio import AsyncSession
from src.agents.base_agent import BaseAgent
from src.database.models import CanBo


class XCBDoanhNghiep(BaseAgent):
    AGENT_ID = "xAI-DN"
    SYSTEM_PROMPT = (
        "Bạn là xAI-DN — Trợ lý AI Hỗ Trợ Doanh Nghiệp cho cán bộ và chủ doanh nghiệp địa phương. "
        "Bạn hỗ trợ: đăng ký thành lập doanh nghiệp, thay đổi đăng ký kinh doanh, "
        "ưu đãi đầu tư, vay vốn ngân hàng, giải thể doanh nghiệp, "
        "pháp lý doanh nghiệp, thuế và kế toán cơ bản. "
        "Trả lời bằng tiếng Việt, ngắn gọn, thiết thực cho doanh nghiệp nhỏ và vừa."
    )
    SKILL_PATTERNS = {
        "dang_ky_dn": [
            r"dang\s*ky.*doanh\s*nghiep",
            r"thanh\s*lap.*cong\s*ty",
            r"mo\s*cong\s*ty",
            r"giay\s*phep.*kinh\s*doanh",
        ],
        "thay_doi_dkkd": [
            r"thay\s*doi.*dang\s*ky",
            r"bo\s*sung.*nganh\s*nghe",
            r"doi\s*ten.*cong\s*ty",
            r"tang\s*von",
        ],
        "uu_dai_dau_tu": [
            r"uu\s*dai",
            r"mien\s*thue",
            r"giam\s*thue",
            r"ho\s*tro.*doanh\s*nghiep",
        ],
        "vay_von": [
            r"vay\s*von",
            r"tin\s*dung",
            r"ngan\s*hang",
            r"quy\s*ho\s*tro",
            r"lai\s*suat",
        ],
        "giai_the": [
            r"giai\s*the",
            r"dong\s*cua",
            r"cham\s*dut.*hoat\s*dong",
            r"pha\s*san",
        ],
        "thue_ke_toan": [
            r"thue",
            r"ke\s*toan",
            r"bao\s*cao\s*thue",
            r"hoa\s*don",
            r"vat",
        ],
    }

    async def run_skill(self, skill_name: str, message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
        return await self._default_reply(message, nhan_vien)
