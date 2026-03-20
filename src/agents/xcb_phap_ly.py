"""
src/agents/xcb_phap_ly.py — xAI-PL: Agent Pháp Lý
Nghiệp vụ: Văn bản pháp luật, Nghị định, Thông tư, Tra cứu quy định pháp lý
"""
from sqlalchemy.ext.asyncio import AsyncSession
from src.agents.base_agent import BaseAgent
from src.database.models import CanBo


class XCBPhapLy(BaseAgent):
    AGENT_ID = "xAI-PL"
    SYSTEM_PROMPT = (
        "Bạn là xAI-PL — Trợ lý AI Pháp Lý cho cán bộ công chức địa phương (cấp Tỉnh/Huyện/Xã). "
        "Bạn hỗ trợ: tra cứu văn bản pháp luật, giải thích Luật, Nghị định, Thông tư, "
        "tư vấn áp dụng quy định pháp lý vào thực tiễn hành chính. "
        "Luôn trích dẫn số hiệu văn bản pháp quy cụ thể. Trả lời bằng tiếng Việt, ngắn gọn, chính xác."
    )
    SKILL_PATTERNS = {
        "tra_cuu_van_ban": [
            r"tra\s*cuu",
            r"van\s*ban",
            r"nghi\s*dinh",
            r"thong\s*tu",
            r"quyet\s*dinh",
            r"luat\s*\w+",
            r"so\s+\d+/\d+",
        ],
        "giai_thich_luat": [
            r"giai\s*thich",
            r"hieu\s*the\s*nao",
            r"quy\s*dinh.*la\s*gi",
            r"co\s*nghia\s*la",
            r"ap\s*dung.*nhu\s*the\s*nao",
        ],
        "kiem_tra_hieu_luc": [
            r"con\s*hieu\s*luc",
            r"da\s*het\s*hieu\s*luc",
            r"duoc\s*sua\s*doi",
            r"thay\s*the.*bang",
            r"bai\s*bo",
        ],
        "tu_van_xu_ly": [
            r"xu\s*ly.*nhu\s*the\s*nao",
            r"phai\s*lam\s*gi",
            r"co\s*vi\s*pham",
            r"xu\s*phat",
            r"khieu\s*nai",
            r"khieu\s*kien",
        ],
        "tuyen_truyen_phap_luat": [
            r"tuyen\s*truyen",
            r"giao\s*duc.*phap\s*luat",
            r"pho\s*bien",
            r"nhan\s*thuc.*phap\s*luat",
        ],
    }

    async def run_skill(
        self, skill_name: str, message: str, nhan_vien: CanBo, db: AsyncSession
    ) -> str:
        return await self._default_reply(message, nhan_vien)
