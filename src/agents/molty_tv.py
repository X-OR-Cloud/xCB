"""
src/agents/molty_tv.py — MOLTY-TV: Agent Thuyền viên / Hàn Quốc
Phòng: thuy_en_vien, han_quoc
"""
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.base_agent import BaseAgent
from src.database.models import NhanVien
from src.skills.thuy_en_vien import skills as tv_skills


class MoltyTV(BaseAgent):
    AGENT_ID = "MOLTY-TV"
    SYSTEM_PROMPT = (
        "Bạn là MOLTY-TV — trợ lý AI chuyên về thuyền viên và thị trường lao động Hàn Quốc của Thinh Long Group. "
        "Bạn hỗ trợ: quản lý đơn hàng tàu, hồ sơ thuyền viên, bằng cấp hàng hải, thị trường Hàn Quốc. "
        "Luôn trả lời bằng tiếng Việt, ngắn gọn và chuyên nghiệp."
    )
    SKILL_PATTERNS = {
        "don_hang_tau": [
            r"don\s*hang",
            r"tau",
            r"chu\s*tau",
            r"vi\s*tri.*tau",
        ],
        "ho_so_thuyen_vien": [
            r"thuyen\s*vien",
            r"bang\s*cap.*hang\s*hai",
            r"chung\s*chi.*tau",
        ],
        "thi_truong_han_quoc": [
            r"han\s*quoc",
            r"eps",
            r"thi\s*truong.*han",
            r"bao\s*cao.*han",
        ],
        "lich_khoi_hanh": [
            r"khoi\s*hanh",
            r"lich.*di.*lam",
            r"xuat\s*canh",
        ],
    }

    async def run_skill(self, skill_name: str, message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
        handler = {
            "don_hang_tau":      tv_skills.don_hang_tau,
            "ho_so_thuyen_vien": tv_skills.ho_so_thuyen_vien,
            "thi_truong_han_quoc": tv_skills.thi_truong_han_quoc,
            "lich_khoi_hanh":    tv_skills.lich_khoi_hanh,
        }.get(skill_name)

        if handler:
            return await handler(message=message, nhan_vien=nhan_vien, db=db)
        return await self._default_reply(message, nhan_vien)
