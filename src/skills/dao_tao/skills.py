"""
src/skills/dao_tao/skills.py — Skills cho xAI-GD (Giáo dục / Đào tạo)
Lưu ý: Các skill gốc từ xHR (DiemDanh, HocVienLop, LopHoc, TinhTrangLopHoc)
đã được thay thế bằng stub. Hệ thống xCB chưa có các model tương ứng.
"""
from datetime import date

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import CanBo

log = structlog.get_logger(__name__)


async def diem_danh(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Stub — Tính năng điểm danh chưa được triển khai cho xCB."""
    return (
        "📋 Tính năng điểm danh học viên "
        "đang được phát triển cho hệ thống xCB.\n"
        "Vui lòng liên hệ quản trị viên để biết thêm chi tiết."
    )


async def lich_hoc(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Stub — Tính năng lịch học chưa được triển khai cho xCB."""
    return (
        "📅 Tính năng quản lý lịch học "
        "đang được phát triển cho hệ thống xCB.\n"
        "Vui lòng liên hệ quản trị viên để biết thêm chi tiết."
    )


async def ket_qua_hoc(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Stub — Tính năng kết quả học chưa được triển khai cho xCB."""
    return (
        "🎓 Tính năng tra cứu kết quả học viên "
        "đang được phát triển cho hệ thống xCB.\n"
        "Vui lòng liên hệ quản trị viên để biết thêm chi tiết."
    )


async def bao_cao_dao_tao(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Stub — Tính năng báo cáo đào tạo chưa được triển khai cho xCB."""
    return (
        "📊 Tính năng báo cáo trung tâm đào tạo "
        "đang được phát triển cho hệ thống xCB.\n"
        "Vui lòng liên hệ quản trị viên để biết thêm chi tiết."
    )
