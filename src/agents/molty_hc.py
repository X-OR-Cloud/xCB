"""
src/agents/molty_hc.py — MOLTY-HC: Agent Hành chính / Kế toán
Phòng: hanh_chinh, ke_toan
"""
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.base_agent import BaseAgent
from src.database.models import NhanVien
from src.skills.hanh_chinh import skills as hc_skills


class MoltyHC(BaseAgent):
    AGENT_ID = "MOLTY-HC"
    SYSTEM_PROMPT = (
        "Bạn là MOLTY-HC — trợ lý AI cho phòng Hành chính & Kế toán Thinh Long Group. "
        "Bạn hỗ trợ: hợp đồng lao động, quản lý nhân viên, trình ký, BHXH, phí & thanh toán. "
        "Luôn trả lời bằng tiếng Việt, ngắn gọn và chuyên nghiệp."
    )
    SKILL_PATTERNS = {
        "trinh_ky": [
            r"trinh\s*ky",
            r"phe\s*duyet",
            r"can\s*ky",
            r"cho\s*duyet",
        ],
        "ho_so_nhan_vien": [
            r"nhan\s*vien",
            r"ho\s*so.*nv",
            r"thong\s*tin.*nv",
        ],
        "phi_thanh_toan": [
            r"phi",
            r"thanh\s*toan",
            r"cong\s*no",
            r"thu\s*phi",
            r"chua\s*dong",
        ],
        "nhac_bhxh": [
            r"bhxh",
            r"bao\s*hiem\s*xa\s*hoi",
            r"dong\s*bao\s*hiem",
        ],
        "hop_dong": [
            r"hop\s*dong",
            r"ky\s*ket",
            r"gia\s*han",
            r"het\s*han.*hop\s*dong",
        ],
    }

    async def run_skill(self, skill_name: str, message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
        handler = {
            "trinh_ky":        hc_skills.trinh_ky,
            "ho_so_nhan_vien": hc_skills.ho_so_nhan_vien,
            "phi_thanh_toan":  hc_skills.phi_thanh_toan,
            "nhac_bhxh":       hc_skills.nhac_bhxh,
            "hop_dong":        hc_skills.hop_dong,
        }.get(skill_name)

        if handler:
            return await handler(message=message, nhan_vien=nhan_vien, db=db)
        return await self._default_reply(message, nhan_vien)
