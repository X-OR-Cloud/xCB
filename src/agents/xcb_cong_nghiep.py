"""
src/agents/xcb_cong_nghiep.py — xAI-CN: Agent Công Nghiệp
"""
from sqlalchemy.ext.asyncio import AsyncSession
from src.agents.base_agent import BaseAgent
from src.database.models import CanBo


class XCBCongNghiep(BaseAgent):
    AGENT_ID = "xAI-CN"
    SYSTEM_PROMPT = (
        "Bạn là xAI-CN — Trợ lý AI Công Nghiệp cho cán bộ quản lý công nghiệp địa phương. "
        "Bạn hỗ trợ: thủ tục cấp phép sản xuất kinh doanh, quản lý Khu Công Nghiệp (KCN), "
        "tiêu chuẩn chất lượng sản phẩm, an toàn lao động, phòng cháy chữa cháy trong công nghiệp, "
        "thu hút đầu tư, quy định xuất nhập khẩu hàng hóa. "
        "Trả lời bằng tiếng Việt, chuyên nghiệp, dẫn chiếu văn bản pháp lý."
    )
    SKILL_PATTERNS = {
        "cap_phep_sx": [
            r"cap\s*phep.*san\s*xuat",
            r"cap\s*phep.*kinh\s*doanh",
            r"dieu\s*kien.*hoat\s*dong",
        ],
        "kcn": [
            r"khu\s*cong\s*nghiep",
            r"kcn",
            r"khu\s*kinh\s*te",
            r"thue\s*dat.*kcn",
        ],
        "tieu_chuan_chat_luong": [
            r"tieu\s*chuan",
            r"chat\s*luong\s*san\s*pham",
            r"iso",
            r"kiem\s*dinh",
            r"chung\s*nhan",
        ],
        "an_toan_lao_dong": [
            r"an\s*toan\s*lao\s*dong",
            r"bao\s*ho\s*lao\s*dong",
            r"phong\s*chay",
            r"chay\s*no",
        ],
        "thu_hut_dau_tu": [
            r"dau\s*tu",
            r"uu\s*dai.*dau\s*tu",
            r"thu\s*hut.*nha\s*dau\s*tu",
            r"moi\s*truong.*dau\s*tu",
        ],
    }

    async def run_skill(self, skill_name: str, message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
        return await self._default_reply(message, nhan_vien)
