"""
src/skills/lanh_dao/skills.py — Skills cho MOLTY-CEO (Lãnh đạo / TGĐ)
"""
from datetime import date, timedelta

import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import (
    AuditLog, HopDong, LaoDong, NhanVien,
    PhiVaThanhToan, TinhTrangHopDong, TinhTrangLaoDong,
    TinhTrangThanhToan, TrinhKy, TinhTrangTrinhKy,
)

log = structlog.get_logger(__name__)


async def dashboard_tong_hop(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Dashboard tổng hợp toàn công ty."""
    # Lao động
    tong_ld = await db.scalar(select(func.count(LaoDong.id))) or 0
    dang_xl = await db.scalar(
        select(func.count(LaoDong.id)).where(LaoDong.tinh_trang == TinhTrangLaoDong.dang_xu_ly)
    ) or 0
    da_xuat = await db.scalar(
        select(func.count(LaoDong.id)).where(LaoDong.tinh_trang == TinhTrangLaoDong.da_xuat_canh)
    ) or 0

    # Nhân viên
    tong_nv = await db.scalar(
        select(func.count(NhanVien.id)).where(NhanVien.dang_lam_viec.is_(True))
    ) or 0

    # Hợp đồng hiệu lực
    tong_hd = await db.scalar(
        select(func.count(HopDong.id)).where(HopDong.tinh_trang == TinhTrangHopDong.hieu_luc)
    ) or 0

    # Phí chưa thu
    tong_phi_chua_thu = await db.scalar(
        select(func.coalesce(func.sum(PhiVaThanhToan.so_tien), 0)).where(
            PhiVaThanhToan.tinh_trang == TinhTrangThanhToan.chua_thanh_toan
        )
    ) or 0

    # Trình ký chờ duyệt
    cho_duyet = await db.scalar(
        select(func.count(TrinhKy.id)).where(TrinhKy.tinh_trang == TinhTrangTrinhKy.cho_duyet)
    ) or 0

    return (
        f"📊 *DASHBOARD TỔNG HỢP — THINH LONG GROUP*\n"
        f"📅 Ngày: {date.today().strftime('%d/%m/%Y')}\n"
        f"{'─' * 35}\n\n"
        f"👷 *Lao động xuất khẩu*\n"
        f"  • Tổng hồ sơ: *{tong_ld}*\n"
        f"  • Đã xuất cảnh: *{da_xuat}*\n"
        f"  • Đang xử lý: *{dang_xl}*\n\n"
        f"👥 *Nhân sự nội bộ:* {tong_nv} nhân viên\n\n"
        f"📋 *Hợp đồng hiệu lực:* {tong_hd}\n\n"
        f"💰 *Phí chưa thu:* {tong_phi_chua_thu:,.0f} VND\n\n"
        f"📝 *Trình ký chờ duyệt:* {cho_duyet} văn bản"
    )


async def canh_bao_rui_ro(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Tổng hợp cảnh báo rủi ro."""
    today = date.today()
    warnings = []

    # HĐ sắp hết hạn 30 ngày
    hd_het_han = await db.scalar(
        select(func.count(HopDong.id)).where(
            HopDong.tinh_trang == TinhTrangHopDong.hieu_luc,
            HopDong.ngay_het_han <= today + timedelta(days=30),
            HopDong.ngay_het_han >= today,
        )
    ) or 0
    if hd_het_han:
        warnings.append(f"⚠️ *{hd_het_han} hợp đồng* hết hạn trong 30 ngày")

    # Phi quá hạn
    phi_qua_han = await db.scalar(
        select(func.count(PhiVaThanhToan.id)).where(
            PhiVaThanhToan.tinh_trang == TinhTrangThanhToan.qua_han
        )
    ) or 0
    if phi_qua_han:
        warnings.append(f"🔴 *{phi_qua_han} khoản phí* quá hạn chưa thu")

    # Trình ký quá hạn
    tk_qua_han = await db.scalar(
        select(func.count(TrinhKy.id)).where(
            TrinhKy.tinh_trang == TinhTrangTrinhKy.cho_duyet,
            TrinhKy.han_duyet < today,
        )
    ) or 0
    if tk_qua_han:
        warnings.append(f"🔴 *{tk_qua_han} văn bản trình ký* đã quá hạn duyệt")

    if not warnings:
        return "✅ *Không có cảnh báo rủi ro nào. Mọi thứ đang trong tầm kiểm soát.*"

    lines = [f"🚨 *CẢNH BÁO RỦI RO — {today.strftime('%d/%m/%Y')}*\n"]
    lines.extend(warnings)
    return "\n".join(lines)


async def bao_cao_tai_chinh(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Báo cáo tài chính tổng hợp."""
    from src.database.models import LoaiPhi

    # Tổng phí cần thu
    tong_can_thu = await db.scalar(
        select(func.coalesce(func.sum(PhiVaThanhToan.so_tien), 0))
    ) or 0

    # Đã thu
    da_thu = await db.scalar(
        select(func.coalesce(func.sum(PhiVaThanhToan.so_tien), 0)).where(
            PhiVaThanhToan.tinh_trang == TinhTrangThanhToan.da_thanh_toan
        )
    ) or 0

    chua_thu = float(tong_can_thu) - float(da_thu)
    ty_le = (float(da_thu) / float(tong_can_thu) * 100) if tong_can_thu else 0

    return (
        f"💰 *BÁO CÁO TÀI CHÍNH*\n"
        f"{'─' * 30}\n\n"
        f"• Tổng phí phải thu: *{float(tong_can_thu):,.0f} VND*\n"
        f"• Đã thu: *{float(da_thu):,.0f} VND* ({ty_le:.1f}%)\n"
        f"• Chưa thu: *{chua_thu:,.0f} VND*\n\n"
        f"📈 Tỷ lệ thu: *{ty_le:.1f}%*"
    )


async def tinh_hinh_xuat_khau(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Tình hình xuất khẩu lao động theo thị trường."""
    result = await db.execute(
        select(LaoDong.thi_truong, func.count(LaoDong.id).label("so_luong"))
        .group_by(LaoDong.thi_truong)
        .order_by(func.count(LaoDong.id).desc())
    )
    rows = result.all()

    tong = sum(r.so_luong for r in rows)
    lines = [f"✈️ *TÌNH HÌNH XUẤT KHẨU LAO ĐỘNG*\n📅 {date.today().strftime('%d/%m/%Y')}\n"]
    for r in rows:
        pct = (r.so_luong / tong * 100) if tong else 0
        lines.append(f"• 🌏 *{r.thi_truong.upper()}*: {r.so_luong} người ({pct:.1f}%)")
    lines.append(f"\n*Tổng cộng: {tong} hồ sơ*")
    return "\n".join(lines)
