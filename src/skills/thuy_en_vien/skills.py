"""
src/skills/thuy_en_vien/skills.py — Skills cho thuyền viên / Hàn Quốc
Lưu ý: Các skill gốc từ xHR (LaoDong, ThuyEnVienDonHang, TinhTrangDonHang, TinhTrangLaoDong)
đã được thay thế bằng stub. Hệ thống xCB chưa có các model tương ứng.
"""
from datetime import date

import structlog
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import CanBo

log = structlog.get_logger(__name__)


async def don_hang_tau(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Stub — Tính năng đơn hàng tàu chưa được triển khai cho xCB."""
    return (
        "🚢 Tính năng quản lý đơn hàng thuyền viên "
        "đang được phát triển cho hệ thống xCB.\n"
        "Vui lòng liên hệ quản trị viên để biết thêm chi tiết."
    )


async def ho_so_thuyen_vien(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Stub — Tính năng hồ sơ thuyền viên chưa được triển khai cho xCB."""
    return (
        "⚓ Tính năng tra cứu hồ sơ thuyền viên "
        "đang được phát triển cho hệ thống xCB.\n"
        "Vui lòng liên hệ quản trị viên để biết thêm chi tiết."
    )


async def thi_truong_han_quoc(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Stub — Tính năng thị trường Hàn Quốc chưa được triển khai cho xCB."""
    return (
        "🇰🇷 Tính năng báo cáo thị trường Hàn Quốc "
        "đang được phát triển cho hệ thống xCB.\n"
        "Vui lòng liên hệ quản trị viên để biết thêm chi tiết."
    )


async def lich_khoi_hanh(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Stub — Tính năng lịch khởi hành chưa được triển khai cho xCB."""
    return (
        "📅 Tính năng quản lý lịch xuất cảnh "
        "đang được phát triển cho hệ thống xCB.\n"
        "Vui lòng liên hệ quản trị viên để biết thêm chi tiết."
    )
