"""
src/agents/molty_ceo.py — MOLTY-CEO: Agent Lãnh đạo / TGĐ
Phòng: lanh_dao, tgd
"""
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.base_agent import BaseAgent
from src.database.models import NhanVien
from src.skills.lanh_dao import skills as ceo_skills


class MoltyCEO(BaseAgent):
    AGENT_ID = "MOLTY-CEO"
    SYSTEM_PROMPT = (
        "Bạn là MOLTY-CEO — trợ lý AI cho Ban Lãnh đạo & TGĐ Thinh Long Group. "
        "Bạn cung cấp: dashboard tổng hợp, báo cáo KPI toàn công ty, tóm tắt pipeline xuất khẩu, "
        "cảnh báo rủi ro, số liệu tài chính. Trình bày súc tích, dùng bảng và bullet points. "
        "Luôn trả lời bằng tiếng Việt."
    )
    SKILL_PATTERNS = {
        "dashboard_tong_hop": [
            r"dashboard",
            r"tong\s*quan",
            r"bao\s*cao\s*toan\s*cong\s*ty",
            r"kpi",
            r"so\s*lieu.*tong",
        ],
        "canh_bao_rui_ro": [
            r"rui\s*ro",
            r"canh\s*bao",
            r"van\s*de",
            r"su\s*co",
        ],
        "bao_cao_tai_chinh": [
            r"tai\s*chinh",
            r"doanh\s*thu",
            r"chi\s*phi",
            r"loi\s*nhuan",
            r"phi.*thu\s*duoc",
        ],
        "tinh_hinh_xuat_khau": [
            r"xuat\s*khau",
            r"lao\s*dong.*xuat\s*canh",
            r"chi\s*tieu",
            r"ke\s*hoach.*nam",
        ],
    }

    async def run_skill(self, skill_name: str, message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
        handler = {
            "dashboard_tong_hop":  ceo_skills.dashboard_tong_hop,
            "canh_bao_rui_ro":     ceo_skills.canh_bao_rui_ro,
            "bao_cao_tai_chinh":   ceo_skills.bao_cao_tai_chinh,
            "tinh_hinh_xuat_khau": ceo_skills.tinh_hinh_xuat_khau,
        }.get(skill_name)

        if handler:
            return await handler(message=message, nhan_vien=nhan_vien, db=db)
        return await self._default_reply(message, nhan_vien)
