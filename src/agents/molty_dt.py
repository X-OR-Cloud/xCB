"""
src/agents/molty_dt.py — MOLTY-DT: Agent Đào tạo
Phòng: dao_tao
"""
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.base_agent import BaseAgent
from src.database.models import NhanVien
from src.skills.dao_tao import skills as dt_skills


class MoltyDT(BaseAgent):
    AGENT_ID = "MOLTY-DT"
    SYSTEM_PROMPT = (
        "Bạn là MOLTY-DT — trợ lý AI cho Trung tâm Đào tạo Thinh Long Group. "
        "Bạn hỗ trợ: quản lý lớp học, điểm danh, kết quả học viên, lịch học, báo cáo đào tạo. "
        "Luôn trả lời bằng tiếng Việt, ngắn gọn và chuyên nghiệp."
    )
    SKILL_PATTERNS = {
        "diem_danh": [
            r"diem\s*danh",
            r"co\s*mat",
            r"vang\s*mat",
            r"di\s*hoc",
        ],
        "lich_hoc": [
            r"lich\s*hoc",
            r"thoi\s*khoa\s*bieu",
            r"lop\s*hoc",
            r"hom\s*nay.*hoc",
        ],
        "ket_qua_hoc": [
            r"diem",
            r"ket\s*qua",
            r"kiem\s*tra",
            r"thi\s*cuoi\s*khoa",
            r"xep\s*loai",
        ],
        "bao_cao_dao_tao": [
            r"bao\s*cao.*dao\s*tao",
            r"thong\s*ke.*hoc\s*vien",
            r"ty\s*le.*hoan\s*thanh",
        ],
    }

    async def run_skill(self, skill_name: str, message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
        handler = {
            "diem_danh":       dt_skills.diem_danh,
            "lich_hoc":        dt_skills.lich_hoc,
            "ket_qua_hoc":     dt_skills.ket_qua_hoc,
            "bao_cao_dao_tao": dt_skills.bao_cao_dao_tao,
        }.get(skill_name)

        if handler:
            return await handler(message=message, nhan_vien=nhan_vien, db=db)
        return await self._default_reply(message, nhan_vien)
