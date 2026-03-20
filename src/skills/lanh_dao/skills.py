"""
src/skills/lanh_dao/skills.py — Skills cho xAI-GM (Giám sát / Lãnh đạo)
Lưu ý: Các skill gốc từ xHR (HopDong, LaoDong, PhiVaThanhToan, TrinhKy, etc.)
đã được thay thế bằng stub. Hệ thống xCB sử dụng CanBo và HoSoHanhChinh.
"""
from datetime import date, timedelta

import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import (
    AuditLog, CanBo, HoSoHanhChinh, TrangThaiHoSo,
)

log = structlog.get_logger(__name__)


async def dashboard_tong_hop(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Dashboard tổng hợp cho lãnh đạo — dựa trên dữ liệu xCB."""
    # Cán bộ
    tong_cb = await db.scalar(
        select(func.count(CanBo.id)).where(CanBo.dang_cong_tac.is_(True))
    ) or 0

    # Hồ sơ hành chính
    tong_hs = await db.scalar(select(func.count(HoSoHanhChinh.id))) or 0
    dang_xu_ly = await db.scalar(
        select(func.count(HoSoHanhChinh.id)).where(
            HoSoHanhChinh.trang_thai == TrangThaiHoSo.dang_xu_ly
        )
    ) or 0
    hoan_thanh = await db.scalar(
        select(func.count(HoSoHanhChinh.id)).where(
            HoSoHanhChinh.trang_thai == TrangThaiHoSo.hoan_thanh
        )
    ) or 0
    qua_han = await db.scalar(
        select(func.count(HoSoHanhChinh.id)).where(
            HoSoHanhChinh.trang_thai == TrangThaiHoSo.qua_han
        )
    ) or 0

    return (
        f"📊 *DASHBOARD TỔNG HỢP — xCB*\n"
        f"📅 Ngày: {date.today().strftime('%d/%m/%Y')}\n"
        f"{'─' * 35}\n\n"
        f"👥 *Cán bộ đang công tác:* {tong_cb}\n\n"
        f"📋 *Hồ sơ hành chính*\n"
        f"  • Tổng hồ sơ: *{tong_hs}*\n"
        f"  • Đang xử lý: *{dang_xu_ly}*\n"
        f"  • Hoàn thành: *{hoan_thanh}*\n"
        f"  • Quá hạn: *{qua_han}*"
    )


async def canh_bao_rui_ro(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Tổng hợp cảnh báo rủi ro — dựa trên hồ sơ quá hạn."""
    today = date.today()
    warnings = []

    # Hồ sơ quá hạn
    hs_qua_han = await db.scalar(
        select(func.count(HoSoHanhChinh.id)).where(
            HoSoHanhChinh.trang_thai == TrangThaiHoSo.qua_han
        )
    ) or 0
    if hs_qua_han:
        warnings.append(f"🔴 *{hs_qua_han} hồ sơ* đã quá hạn xử lý")

    # Hồ sơ sắp hết hạn (trong 3 ngày)
    hs_sap_het_han = await db.scalar(
        select(func.count(HoSoHanhChinh.id)).where(
            HoSoHanhChinh.trang_thai == TrangThaiHoSo.dang_xu_ly,
            HoSoHanhChinh.han_tra_ket_qua <= today + timedelta(days=3),
            HoSoHanhChinh.han_tra_ket_qua >= today,
        )
    ) or 0
    if hs_sap_het_han:
        warnings.append(f"⚠️ *{hs_sap_het_han} hồ sơ* sắp hết hạn trong 3 ngày")

    if not warnings:
        return "✅ *Không có cảnh báo rủi ro nào. Mọi thứ đang trong tầm kiểm soát.*"

    lines = [f"🚨 *CẢNH BÁO RỦI RO — {today.strftime('%d/%m/%Y')}*\n"]
    lines.extend(warnings)
    return "\n".join(lines)


async def bao_cao_tai_chinh(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Stub — Tính năng báo cáo tài chính chưa được triển khai cho xCB."""
    return (
        "💰 Tính năng báo cáo tài chính đang được phát triển cho hệ thống xCB.\n"
        "Vui lòng liên hệ quản trị viên để biết thêm chi tiết."
    )


async def tinh_hinh_xuat_khau(message: str, nhan_vien: CanBo, db: AsyncSession) -> str:
    """Stub — Tính năng xuất khẩu lao động chưa được triển khai cho xCB."""
    return (
        "✈️ Tính năng báo cáo xuất khẩu lao động đang được phát triển cho hệ thống xCB.\n"
        "Vui lòng liên hệ quản trị viên để biết thêm chi tiết."
    )
