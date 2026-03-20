"""
src/agents/xcb_giam_sat.py — xAI-GM: Agent Giám Sát & Tổng Hợp
"""
from sqlalchemy.ext.asyncio import AsyncSession
from src.agents.base_agent import BaseAgent
from src.database.models import CanBo


class XCBGiamSat(BaseAgent):
    AGENT_ID = "xAI-GM"
    SYSTEM_PROMPT = (
        "Bạn là xAI-GM — Trợ lý AI Giám Sát & Tổng Hợp cho lãnh đạo đơn vị hành chính. "
        "Bạn cung cấp: dashboard chỉ tiêu xử lý hồ sơ hành chính, báo cáo KPI đơn vị, "
        "cảnh báo hồ sơ quá hạn, thống kê theo nghiệp vụ và thời kỳ, "
        "phân tích hiệu quả hoạt động của đơn vị. "
        "Trình bày súc tích, dùng bảng và số liệu. Trả lời bằng tiếng Việt."
    )
    SKILL_PATTERNS = {
        "dashboard_tong_hop": [
            r"dashboard",
            r"tong\s*quan",
            r"bao\s*cao\s*toan",
            r"kpi",
            r"chi\s*tieu",
        ],
        "canh_bao_qua_han": [
            r"qua\s*han",
            r"tre\s*han",
            r"canh\s*bao",
            r"ho\s*so.*chua\s*xu\s*ly",
        ],
        "bao_cao_thong_ke": [
            r"thong\s*ke",
            r"bao\s*cao.*thang",
            r"so\s*lieu",
            r"ty\s*le\s*hoan\s*thanh",
        ],
        "hieu_qua_hoat_dong": [
            r"hieu\s*qua",
            r"nang\s*suat",
            r"danh\s*gia.*don\s*vi",
            r"xep\s*hang",
        ],
    }

    async def run_skill(self, skill_name: str, message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
        return await self._default_reply(message, nhan_vien)
