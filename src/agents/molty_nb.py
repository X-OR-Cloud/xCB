"""
src/agents/molty_nb.py — MOLTY-NB: Agent thị trường Nhật Bản
Phòng: nhat_ban
"""
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents.base_agent import BaseAgent
from src.database.models import NhanVien
from src.skills.nhat_ban import skills as nb_skills


class MoltyNB(BaseAgent):
    AGENT_ID = "MOLTY-NB"
    SYSTEM_PROMPT = (
        "Bạn là MOLTY-NB — trợ lý AI chuyên về thị trường lao động Nhật Bản của Thinh Long Group. "
        "Bạn hỗ trợ các nghiệp vụ: quản lý hồ sơ lao động sang Nhật, theo dõi pipeline xuất khẩu, "
        "tình trạng visa/hộ chiếu, báo cáo số liệu thị trường Nhật. "
        "Luôn trả lời bằng tiếng Việt, ngắn gọn và chuyên nghiệp."
    )
    SKILL_PATTERNS = {
        "xem_ho_so": [
            r"ho\s*so",
            r"xem.*lao.*dong",
            r"thong\s*tin.*lao.*dong",
            r"tra\s*cuu",
        ],
        "tien_do_pipeline": [
            r"tien\s*do",
            r"pipeline",
            r"quy\s*trinh",
            r"buoc.*xu\s*ly",
        ],
        "het_han_ho_chieu": [
            r"ho\s*chieu",
            r"het\s*han",
            r"visa",
            r"giay\s*to",
        ],
        "bao_cao_thi_truong": [
            r"bao\s*cao",
            r"thong\s*ke",
            r"so\s*lieu",
            r"thi\s*truong\s*nhat",
        ],
    }

    async def run_skill(self, skill_name: str, message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
        handler = {
            "xem_ho_so":         nb_skills.xem_ho_so,
            "tien_do_pipeline":  nb_skills.tien_do_pipeline,
            "het_han_ho_chieu":  nb_skills.het_han_ho_chieu,
            "bao_cao_thi_truong": nb_skills.bao_cao_thi_truong,
        }.get(skill_name)

        if handler:
            return await handler(message=message, nhan_vien=nhan_vien, db=db)
        return await self._default_reply(message, nhan_vien)
