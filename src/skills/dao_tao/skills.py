"""
src/skills/dao_tao/skills.py — Skills cho MOLTY-DT (Trung tâm Đào tạo)
"""
from datetime import date

import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import DiemDanh, HocVienLop, LopHoc, NhanVien, TinhTrangLopHoc

log = structlog.get_logger(__name__)


async def diem_danh(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Báo cáo điểm danh hôm nay."""
    today = date.today()
    result = await db.execute(
        select(DiemDanh, LopHoc)
        .join(LopHoc, DiemDanh.lop_hoc_id == LopHoc.id)
        .where(DiemDanh.ngay == today)
        .order_by(LopHoc.ten_lop.asc())
    )
    rows = result.all()

    if not rows:
        return f"📋 Chưa có dữ liệu điểm danh ngày {today}."

    tong = len(rows)
    co_mat = sum(1 for d, _ in rows if d.co_mat)
    vang = tong - co_mat

    lines = [
        f"📋 *Điểm danh ngày {today}*\n",
        f"✅ Có mặt: *{co_mat}/{tong}*  |  ❌ Vắng: *{vang}*\n",
    ]
    for dd, lop in rows[:15]:
        trang_thai = "✅" if dd.co_mat else "❌"
        tre = f" (trễ {dd.phut_tre} phút)" if dd.phut_tre else ""
        lines.append(f"• {trang_thai} Lớp *{lop.ten_lop}*{tre}")

    return "\n".join(lines)


async def lich_hoc(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Lịch học các lớp đang mở."""
    result = await db.execute(
        select(LopHoc)
        .where(
            LopHoc.tinh_trang.in_([TinhTrangLopHoc.mo, TinhTrangLopHoc.dang_hoc]),
            LopHoc.ngay_bat_dau >= date.today(),
        )
        .order_by(LopHoc.ngay_bat_dau.asc())
        .limit(10)
    )
    lops = result.scalars().all()

    if not lops:
        return "📅 Không có lớp học nào sắp khai giảng."

    lines = ["📅 *Lịch học sắp tới:*\n"]
    for lop in lops:
        lines.append(
            f"• *{lop.ten_lop}* — {lop.mon_hoc}\n"
            f"  👨‍🏫 GV: {lop.giao_vien or 'TBD'} | 🏫 Phòng: {lop.phong_hoc or 'TBD'}\n"
            f"  📆 {lop.ngay_bat_dau} → {lop.ngay_ket_thuc}"
        )
    return "\n\n".join(lines)


async def ket_qua_hoc(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Kết quả học viên các lớp đã kết thúc."""
    result = await db.execute(
        select(HocVienLop, LopHoc)
        .join(LopHoc, HocVienLop.lop_hoc_id == LopHoc.id)
        .where(LopHoc.tinh_trang == TinhTrangLopHoc.ket_thuc)
        .order_by(HocVienLop.diem_cuoi_khoa.desc())
        .limit(15)
    )
    rows = result.all()

    if not rows:
        return "📊 Chưa có kết quả học viên."

    lines = ["🎓 *Kết quả học viên (lớp đã kết thúc):*\n"]
    for hv, lop in rows:
        diem = f"{hv.diem_cuoi_khoa:.1f}" if hv.diem_cuoi_khoa else "N/A"
        lines.append(
            f"• Lớp *{lop.ten_lop}* — ID:{hv.lao_dong_id} "
            f"| Điểm: *{diem}* | Xếp loại: {hv.xep_loai or 'N/A'}"
        )
    return "\n".join(lines)


async def bao_cao_dao_tao(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Báo cáo tổng hợp đào tạo."""
    tong_lop = await db.scalar(select(func.count(LopHoc.id)))
    dang_hoc = await db.scalar(
        select(func.count(LopHoc.id)).where(LopHoc.tinh_trang == TinhTrangLopHoc.dang_hoc)
    )
    tong_hv = await db.scalar(select(func.count(HocVienLop.id)))
    hom_nay_co_mat = await db.scalar(
        select(func.count(DiemDanh.id)).where(
            DiemDanh.ngay == date.today(),
            DiemDanh.co_mat.is_(True),
        )
    )

    return (
        f"📊 *Báo cáo Trung tâm Đào tạo*\n\n"
        f"• Tổng số lớp: *{tong_lop}*\n"
        f"• Đang học: *{dang_hoc}*\n"
        f"• Tổng học viên: *{tong_hv}*\n"
        f"• Có mặt hôm nay: *{hom_nay_co_mat}*"
    )
