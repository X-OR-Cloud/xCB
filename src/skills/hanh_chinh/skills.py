"""
src/skills/hanh_chinh/skills.py — Skills cho xAI-HC (Hành chính công)
Lưu ý: Các skill gốc từ xHR (HopDong, NhanVien, PhiVaThanhToan, TrinhKy)
đã được thay thế bằng stub. Hệ thống xCB sử dụng CanBo và HoSoHanhChinh.
"""
from datetime import date, timedelta

import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import CanBo, HoSoHanhChinh, TrangThaiHoSo

log = structlog.get_logger(__name__)


async def trinh_ky(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Stub — Tính năng trình ký chưa được triển khai cho xCB."""
    return (
        "📝 Tính năng trình ký văn bản đang được phát triển cho hệ thống xCB.\n"
        "Vui lòng liên hệ quản trị viên để biết thêm chi tiết."
    )


async def ho_so_nhan_vien(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Hiển thị danh sách cán bộ đang công tác."""
    result = await db.execute(
        select(CanBo)
        .where(CanBo.dang_cong_tac.is_(True))
        .order_by(CanBo.linh_vuc.asc(), CanBo.ho_ten.asc())
    )
    cb_list = result.scalars().all()

    if not cb_list:
        return "📋 Chưa có dữ liệu cán bộ."

    lines = [f"👥 *Danh sách cán bộ ({len(cb_list)} người):*\n"]
    linh_vuc_hien_tai = None
    for cb in cb_list:
        if cb.linh_vuc != linh_vuc_hien_tai:
            linh_vuc_hien_tai = cb.linh_vuc
            lines.append(f"\n*📌 {cb.linh_vuc.value.upper()}*")
        lines.append(f"  • {cb.ho_ten} — {cb.vai_tro.value} | 📞 {cb.so_dien_thoai or 'N/A'}")
    return "\n".join(lines)


async def phi_thanh_toan(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Stub — Tính năng phí thanh toán chưa được triển khai cho xCB."""
    return (
        "💰 Tính năng quản lý phí và thanh toán đang được phát triển cho hệ thống xCB.\n"
        "Vui lòng liên hệ quản trị viên để biết thêm chi tiết."
    )


async def nhac_bhxh(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Nhắc lịch đóng BHXH."""
    today = date.today()
    ngay_dong = today.replace(day=20)
    if ngay_dong < today:
        from calendar import monthrange
        next_month = today.month % 12 + 1
        year = today.year + (1 if today.month == 12 else 0)
        ngay_dong = date(year, next_month, 20)

    con_lai = (ngay_dong - today).days
    tong_cb = await db.scalar(
        select(func.count(CanBo.id)).where(CanBo.dang_cong_tac.is_(True))
    )

    return (
        f"🏦 *Nhắc nhở BHXH*\n\n"
        f"📅 Hạn đóng: *{ngay_dong}* (còn *{con_lai} ngày*)\n"
        f"👥 Số cán bộ cần đóng: *{tong_cb}*\n\n"
        f"⚠️ Vui lòng chuẩn bị danh sách và nộp trước ngày 20 hàng tháng."
    )


async def hop_dong(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Stub — Tính năng hợp đồng chưa được triển khai cho xCB."""
    return (
        "📋 Tính năng quản lý hợp đồng đang được phát triển cho hệ thống xCB.\n"
        "Vui lòng liên hệ quản trị viên để biết thêm chi tiết."
    )
