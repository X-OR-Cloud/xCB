"""
src/skills/nhat_ban/skills.py — Skills cho xAI-DN (Hỗ trợ doanh nghiệp / thị trường)
Lưu ý: Các skill gốc từ xHR (LaoDong, HoSoPhapLy, PipelineTienDo)
đã được thay thế bằng stub. Hệ thống xCB chưa có các model tương ứng.
"""
from datetime import date, timedelta

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import CanBo
from src.integrations.claude_client import ask_claude

log = structlog.get_logger(__name__)


async def xem_ho_so(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Stub — Tính năng hồ sơ lao động chưa được triển khai cho xCB."""
    return (
        "📂 Tính năng tra cứu hồ sơ lao động thị trường Nhật Bản "
        "đang được phát triển cho hệ thống xCB.\n"
        "Vui lòng liên hệ quản trị viên để biết thêm chi tiết."
    )


async def tien_do_pipeline(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Stub — Tính năng pipeline chưa được triển khai cho xCB."""
    return (
        "📊 Tính năng báo cáo tiến độ pipeline "
        "đang được phát triển cho hệ thống xCB.\n"
        "Vui lòng liên hệ quản trị viên để biết thêm chi tiết."
    )


async def het_han_ho_chieu(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Stub — Tính năng cảnh báo hộ chiếu chưa được triển khai cho xCB."""
    return (
        "⚠️ Tính năng cảnh báo hộ chiếu/visa sắp hết hạn "
        "đang được phát triển cho hệ thống xCB.\n"
        "Vui lòng liên hệ quản trị viên để biết thêm chi tiết."
    )


async def bao_cao_thi_truong(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Stub — Tính năng báo cáo thị trường chưa được triển khai cho xCB."""
    return (
        "📈 Tính năng báo cáo số liệu thị trường "
        "đang được phát triển cho hệ thống xCB.\n"
        "Vui lòng liên hệ quản trị viên để biết thêm chi tiết."
    )
