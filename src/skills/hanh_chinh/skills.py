"""
src/skills/hanh_chinh/skills.py — Skills cho MOLTY-HC (Hành chính / Kế toán)
"""
from datetime import date, timedelta

import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import (
    HopDong, NhanVien, PhiVaThanhToan, TinhTrangHopDong,
    TinhTrangThanhToan, TinhTrangTrinhKy, TrinhKy,
)

log = structlog.get_logger(__name__)


async def trinh_ky(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Danh sách văn bản đang chờ phê duyệt."""
    result = await db.execute(
        select(TrinhKy, NhanVien)
        .join(NhanVien, TrinhKy.nguoi_yeu_cau_id == NhanVien.id)
        .where(
            TrinhKy.tinh_trang == TinhTrangTrinhKy.cho_duyet,
            TrinhKy.nguoi_duyet_id == nhan_vien.id,
        )
        .order_by(TrinhKy.han_duyet.asc())
    )
    rows = result.all()

    if not rows:
        return "✅ Không có văn bản nào đang chờ bạn phê duyệt."

    lines = ["📝 *Văn bản chờ phê duyệt:*\n"]
    for tk, nguoi_ycu in rows:
        han = tk.han_duyet.strftime("%d/%m/%Y %H:%M") if tk.han_duyet else "Không có hạn"
        lines.append(
            f"• *#{tk.id}* — {tk.ten_viec}\n"
            f"  👤 Yêu cầu bởi: {nguoi_ycu.ho_ten} | ⏰ Hạn: {han}"
        )
    return "\n\n".join(lines)


async def ho_so_nhan_vien(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Hiển thị danh sách nhân viên đang làm việc."""
    result = await db.execute(
        select(NhanVien)
        .where(NhanVien.dang_lam_viec.is_(True))
        .order_by(NhanVien.phong_ban.asc(), NhanVien.ho_ten.asc())
    )
    nv_list = result.scalars().all()

    if not nv_list:
        return "📋 Chưa có dữ liệu nhân viên."

    lines = [f"👥 *Danh sách nhân viên ({len(nv_list)} người):*\n"]
    phong_ban_hien_tai = None
    for nv in nv_list:
        if nv.phong_ban != phong_ban_hien_tai:
            phong_ban_hien_tai = nv.phong_ban
            lines.append(f"\n*📌 {nv.phong_ban.value.upper()}*")
        lines.append(f"  • {nv.ho_ten} — {nv.vai_tro.value} | 📞 {nv.so_dien_thoai or 'N/A'}")
    return "\n".join(lines)


async def phi_thanh_toan(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Danh sách phí chưa thanh toán / quá hạn."""
    result = await db.execute(
        select(PhiVaThanhToan, HopDong)
        .join(HopDong, PhiVaThanhToan.hop_dong_id == HopDong.id)
        .where(
            PhiVaThanhToan.tinh_trang.in_([
                TinhTrangThanhToan.chua_thanh_toan,
                TinhTrangThanhToan.qua_han,
            ])
        )
        .order_by(PhiVaThanhToan.ngay_den_han.asc())
        .limit(15)
    )
    rows = result.all()

    if not rows:
        return "✅ Không có khoản phí nào cần xử lý."

    lines = ["💰 *Phí chưa thanh toán:*\n"]
    for phi, hd in rows:
        trang_thai = "🔴 QUÁ HẠN" if phi.tinh_trang == TinhTrangThanhToan.qua_han else "🟡 Chưa TT"
        lines.append(
            f"• {trang_thai} — HĐ: {hd.so_hop_dong or f'#{hd.id}'}\n"
            f"  Loại: {phi.loai_phi.value} | "
            f"Số tiền: *{phi.so_tien:,.0f} {phi.tien_te}* | "
            f"Đến hạn: {phi.ngay_den_han or 'N/A'}"
        )
    return "\n\n".join(lines)


async def nhac_bhxh(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Nhắc lịch đóng BHXH."""
    today = date.today()
    ngay_dong = today.replace(day=20)
    if ngay_dong < today:
        from calendar import monthrange
        next_month = today.month % 12 + 1
        year = today.year + (1 if today.month == 12 else 0)
        ngay_dong = date(year, next_month, 20)

    con_lai = (ngay_dong - today).days
    tong_nv = await db.scalar(
        select(func.count(NhanVien.id)).where(NhanVien.dang_lam_viec.is_(True))
    )

    return (
        f"🏦 *Nhắc nhở BHXH*\n\n"
        f"📅 Hạn đóng: *{ngay_dong}* (còn *{con_lai} ngày*)\n"
        f"👥 Số nhân viên cần đóng: *{tong_nv}*\n\n"
        f"⚠️ Vui lòng chuẩn bị danh sách và nộp trước ngày 20 hàng tháng."
    )


async def hop_dong(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Hợp đồng sắp hết hạn trong 60 ngày."""
    threshold = date.today() + timedelta(days=60)
    result = await db.execute(
        select(HopDong)
        .where(
            HopDong.tinh_trang == TinhTrangHopDong.hieu_luc,
            HopDong.ngay_het_han <= threshold,
            HopDong.ngay_het_han >= date.today(),
        )
        .order_by(HopDong.ngay_het_han.asc())
        .limit(15)
    )
    hd_list = result.scalars().all()

    if not hd_list:
        return "✅ Không có hợp đồng nào sắp hết hạn trong 60 ngày tới."

    lines = ["📋 *Hợp đồng sắp hết hạn:*\n"]
    for hd in hd_list:
        con_lai = (hd.ngay_het_han - date.today()).days
        lines.append(
            f"• HĐ *{hd.so_hop_dong or f'#{hd.id}'}* — "
            f"Hết hạn: {hd.ngay_het_han} (còn *{con_lai} ngày*)"
        )
    return "\n".join(lines)
