"""
src/skills/nhat_ban/skills.py — Skills cho MOLTY-NB (thị trường Nhật Bản)
"""
from datetime import date, timedelta

import structlog
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import (
    HoSoPhapLy, LaoDong, LoaiGiayTo, NhanVien,
    PipelineTienDo, TinhTrangLaoDong,
)
from src.integrations.claude_client import ask_claude

log = structlog.get_logger(__name__)


async def xem_ho_so(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Tra cứu hồ sơ lao động thị trường Nhật Bản."""
    result = await db.execute(
        select(LaoDong)
        .where(LaoDong.thi_truong == "nhat_ban")
        .order_by(LaoDong.ngay_tao.desc())
        .limit(10)
    )
    workers = result.scalars().all()

    if not workers:
        return "📂 Chưa có hồ sơ lao động thị trường Nhật Bản nào."

    lines = ["📋 *Danh sách lao động thị trường Nhật Bản (10 gần nhất):*\n"]
    for w in workers:
        lines.append(
            f"• *{w.ho_ten}* — {w.so_ho_chieu or 'Chưa có HC'} "
            f"| Tình trạng: {w.tinh_trang.value}"
        )
    return "\n".join(lines)


async def tien_do_pipeline(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Báo cáo tiến độ pipeline các lao động Nhật Bản."""
    result = await db.execute(
        select(PipelineTienDo, LaoDong)
        .join(LaoDong, PipelineTienDo.lao_dong_id == LaoDong.id)
        .where(LaoDong.thi_truong == "nhat_ban")
        .order_by(PipelineTienDo.ngay_cap_nhat.desc())
        .limit(10)
    )
    rows = result.all()

    if not rows:
        return "📊 Chưa có dữ liệu pipeline thị trường Nhật Bản."

    lines = ["📊 *Tiến độ Pipeline – Nhật Bản:*\n"]
    for tien_do, lao_dong in rows:
        lines.append(
            f"• *{lao_dong.ho_ten}* — Bước {tien_do.buoc_hien_tai} "
            f"| {tien_do.tinh_trang_buoc.value} "
            f"| DK HT: {tien_do.ngay_du_kien_hoan_thanh or 'N/A'}"
        )
    return "\n".join(lines)


async def het_han_ho_chieu(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Cảnh báo hộ chiếu/visa sắp hết hạn trong 90 ngày."""
    threshold = date.today() + timedelta(days=90)
    result = await db.execute(
        select(HoSoPhapLy, LaoDong)
        .join(LaoDong, HoSoPhapLy.lao_dong_id == LaoDong.id)
        .where(
            LaoDong.thi_truong == "nhat_ban",
            HoSoPhapLy.loai_giay_to.in_([LoaiGiayTo.ho_chieu, LoaiGiayTo.visa]),
            HoSoPhapLy.ngay_het_han <= threshold,
            HoSoPhapLy.ngay_het_han >= date.today(),
        )
        .order_by(HoSoPhapLy.ngay_het_han.asc())
    )
    rows = result.all()

    if not rows:
        return "✅ Không có hộ chiếu/visa nào sắp hết hạn trong 90 ngày tới."

    lines = ["⚠️ *Hộ chiếu / Visa sắp hết hạn (≤ 90 ngày):*\n"]
    for doc, lao_dong in rows:
        con_lai = (doc.ngay_het_han - date.today()).days
        lines.append(
            f"• *{lao_dong.ho_ten}* — {doc.loai_giay_to.value} "
            f"| Hết hạn: {doc.ngay_het_han} (còn {con_lai} ngày)"
        )
    return "\n".join(lines)


async def bao_cao_thi_truong(message: str, nhan_vien: NhanVien, db: AsyncSession) -> str:
    """Báo cáo số liệu tổng hợp thị trường Nhật Bản."""
    total_result = await db.execute(
        select(func.count()).where(LaoDong.thi_truong == "nhat_ban")
    )
    total = total_result.scalar_one()

    xuat_canh_result = await db.execute(
        select(func.count()).where(
            LaoDong.thi_truong == "nhat_ban",
            LaoDong.tinh_trang == TinhTrangLaoDong.da_xuat_canh,
        )
    )
    da_xuat_canh = xuat_canh_result.scalar_one()

    dang_xu_ly_result = await db.execute(
        select(func.count()).where(
            LaoDong.thi_truong == "nhat_ban",
            LaoDong.tinh_trang == TinhTrangLaoDong.dang_xu_ly,
        )
    )
    dang_xu_ly = dang_xu_ly_result.scalar_one()

    return (
        f"📈 *Báo cáo thị trường Nhật Bản*\n\n"
        f"• Tổng hồ sơ: *{total}*\n"
        f"• Đã xuất cảnh: *{da_xuat_canh}*\n"
        f"• Đang xử lý: *{dang_xu_ly}*\n"
        f"• Chờ xuất cảnh: *{total - da_xuat_canh - dang_xu_ly}*"
    )
