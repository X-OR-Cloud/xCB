"""
src/skills/thuy_en_vien/skills.py — Skills cho MOLTY-TV (Thuyền viên / Hàn Quốc)
"""
from datetime import date

import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import (
    LaoDong, NhanVien, ThuyEnVienDonHang, TinhTrangDonHang,
)

log = structlog.get_logger(__name__)


async def don_hang_tau(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Hiển thị các đơn hàng tàu đang mở."""
    result = await db.execute(
        select(ThuyEnVienDonHang)
        .where(ThuyEnVienDonHang.tinh_trang.in_([TinhTrangDonHang.mo, TinhTrangDonHang.dang_tuyen]))
        .order_by(ThuyEnVienDonHang.ngay_khoi_hanh_du_kien.asc())
        .limit(10)
    )
    orders = result.scalars().all()

    if not orders:
        return "📋 Hiện không có đơn hàng tàu nào đang mở."

    lines = ["🚢 *Đơn hàng thuyền viên đang tuyển:*\n"]
    for o in orders:
        lines.append(
            f"• *{o.ten_don_hang}* — {o.vi_tri} | {o.ten_chu_tau} ({o.quoc_gia})\n"
            f"  💰 ${o.muc_luong_usd}/tháng | HĐ {o.thoi_gian_hop_dong_thang} tháng "
            f"| Khởi hành: {o.ngay_khoi_hanh_du_kien or 'TBD'} "
            f"| Cần: {o.so_luong_can} người"
        )
    return "\n\n".join(lines)


async def ho_so_thuyen_vien(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Tra cứu hồ sơ thuyền viên."""
    result = await db.execute(
        select(LaoDong)
        .where(LaoDong.thi_truong.in_(["han_quoc", "nhat_ban"]))
        .order_by(LaoDong.ngay_tao.desc())
        .limit(10)
    )
    workers = result.scalars().all()

    if not workers:
        return "📂 Chưa có hồ sơ thuyền viên nào."

    lines = ["⚓ *Hồ sơ thuyền viên:*\n"]
    for w in workers:
        lines.append(
            f"• *{w.ho_ten}* — HC: {w.so_ho_chieu or 'N/A'} "
            f"| Thị trường: {w.thi_truong} | {w.tinh_trang.value}"
        )
    return "\n".join(lines)


async def thi_truong_han_quoc(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Tóm tắt tình hình thị trường Hàn Quốc."""
    from sqlalchemy import func
    from src.database.models import TinhTrangLaoDong

    total = await db.scalar(select(func.count()).where(LaoDong.thi_truong == "han_quoc"))
    da_di = await db.scalar(
        select(func.count()).where(
            LaoDong.thi_truong == "han_quoc",
            LaoDong.tinh_trang == TinhTrangLaoDong.da_xuat_canh,
        )
    )
    return (
        f"🇰🇷 *Thị trường Hàn Quốc*\n\n"
        f"• Tổng hồ sơ: *{total}*\n"
        f"• Đã xuất cảnh: *{da_di}*\n"
        f"• Đang xử lý: *{total - da_di}*"
    )


async def lich_khoi_hanh(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Lịch xuất cảnh sắp tới."""
    from datetime import timedelta
    nguong = date.today() + timedelta(days=30)
    result = await db.execute(
        select(ThuyEnVienDonHang)
        .where(
            ThuyEnVienDonHang.ngay_khoi_hanh_du_kien <= nguong,
            ThuyEnVienDonHang.ngay_khoi_hanh_du_kien >= date.today(),
        )
        .order_by(ThuyEnVienDonHang.ngay_khoi_hanh_du_kien.asc())
    )
    orders = result.scalars().all()

    if not orders:
        return "📅 Không có chuyến khởi hành nào trong 30 ngày tới."

    lines = ["📅 *Lịch khởi hành trong 30 ngày:*\n"]
    for o in orders:
        con_lai = (o.ngay_khoi_hanh_du_kien - date.today()).days
        lines.append(f"• *{o.ten_don_hang}* — {o.ngay_khoi_hanh_du_kien} (còn {con_lai} ngày)")
    return "\n".join(lines)
