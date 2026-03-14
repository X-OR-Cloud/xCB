"""
src/scheduler.py — APScheduler: các tác vụ tự động (điểm danh, nhắc nhở, báo cáo)
"""
from datetime import date, timedelta

import structlog
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import func, select

from src.database.session import AsyncSessionLocal
from src.database.models import (
    HopDong, HoSoPhapLy, LaoDong, LoaiGiayTo, NhanVien,
    PhiVaThanhToan, TinhTrangHopDong, TinhTrangThanhToan,
    TinhTrangTrinhKy, TrinhKy, PhongBan,
)
from src.integrations.telegram_bot import send_message

log = structlog.get_logger(__name__)

VN_TIMEZONE = "Asia/Ho_Chi_Minh"
scheduler = AsyncIOScheduler(timezone=VN_TIMEZONE)


# ─── Helpers ─────────────────────────────────────────────────────────

async def _get_nv_with_telegram(phong_ban: PhongBan | None = None) -> list[NhanVien]:
    """Lấy danh sách nhân viên có telegram_user_id."""
    async with AsyncSessionLocal() as db:
        query = select(NhanVien).where(
            NhanVien.dang_lam_viec.is_(True),
            NhanVien.telegram_user_id.isnot(None),
        )
        if phong_ban:
            query = query.where(NhanVien.phong_ban == phong_ban)
        result = await db.execute(query)
        return result.scalars().all()


async def _broadcast(nhan_viens: list[NhanVien], message: str) -> None:
    """Gửi message đến nhiều nhân viên."""
    for nv in nhan_viens:
        try:
            await send_message(nv.telegram_user_id, message)
        except Exception as exc:
            log.error("broadcast_error", nhan_vien=nv.ho_ten, error=str(exc))


# ─── Job handlers ─────────────────────────────────────────────────────

async def job_diem_danh(session_label: str) -> None:
    """Nhắc điểm danh học viên (6:15, 8:15, 13:15, 19:45)."""
    log.info("job_diem_danh", session=session_label)
    nv_dao_tao = await _get_nv_with_telegram(PhongBan.dao_tao)
    msg = (
        f"📋 *Nhắc điểm danh — {session_label}*\n"
        f"Vui lòng cập nhật điểm danh học viên cho buổi này.\n"
        f"Gõ: `điểm danh` để xem danh sách."
    )
    await _broadcast(nv_dao_tao, msg)


async def job_bao_cao_tuan() -> None:
    """Báo cáo tuần gửi mỗi thứ Sáu 16:00."""
    log.info("job_bao_cao_tuan")
    async with AsyncSessionLocal() as db:
        tong_ld = await db.scalar(select(func.count(LaoDong.id))) or 0
        tong_hd = await db.scalar(
            select(func.count(HopDong.id)).where(HopDong.tinh_trang == TinhTrangHopDong.hieu_luc)
        ) or 0
        cho_duyet = await db.scalar(
            select(func.count(TrinhKy.id)).where(TrinhKy.tinh_trang == TinhTrangTrinhKy.cho_duyet)
        ) or 0

    msg = (
        f"📊 *BÁO CÁO TUẦN — {date.today().strftime('%d/%m/%Y')}*\n"
        f"{'─' * 30}\n"
        f"• Tổng hồ sơ lao động: *{tong_ld}*\n"
        f"• Hợp đồng hiệu lực: *{tong_hd}*\n"
        f"• Trình ký chờ duyệt: *{cho_duyet}*\n\n"
        f"Gõ `dashboard` để xem chi tiết đầy đủ."
    )
    # Gửi cho lãnh đạo
    nv_lanh_dao = await _get_nv_with_telegram(PhongBan.lanh_dao)
    nv_tgd = await _get_nv_with_telegram(PhongBan.tgd)
    await _broadcast(nv_lanh_dao + nv_tgd, msg)


async def job_nhac_bhxh() -> None:
    """Nhắc đóng BHXH ngày 20 hàng tháng lúc 9:00."""
    log.info("job_nhac_bhxh")
    async with AsyncSessionLocal() as db:
        tong_nv = await db.scalar(
            select(func.count(NhanVien.id)).where(NhanVien.dang_lam_viec.is_(True))
        ) or 0

    msg = (
        f"🏦 *NHẮC ĐÓNG BHXH THÁNG {date.today().month}*\n\n"
        f"Hạn đóng: *ngày 20/{date.today().month}/{date.today().year}*\n"
        f"Tổng nhân viên cần đóng: *{tong_nv}*\n\n"
        f"Phòng Kế toán vui lòng chuẩn bị danh sách và chứng từ."
    )
    nv_ke_toan = await _get_nv_with_telegram(PhongBan.ke_toan)
    nv_hanh_chinh = await _get_nv_with_telegram(PhongBan.hanh_chinh)
    await _broadcast(nv_ke_toan + nv_hanh_chinh, msg)


async def job_canh_bao_ho_chieu() -> None:
    """Cảnh báo hộ chiếu sắp hết hạn (ngưỡng 90 ngày) lúc 7:00."""
    log.info("job_canh_bao_ho_chieu")
    threshold = date.today() + timedelta(days=90)

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(HoSoPhapLy, LaoDong)
            .join(LaoDong, HoSoPhapLy.lao_dong_id == LaoDong.id)
            .where(
                HoSoPhapLy.loai_giay_to.in_([LoaiGiayTo.ho_chieu, LoaiGiayTo.visa]),
                HoSoPhapLy.ngay_het_han <= threshold,
                HoSoPhapLy.ngay_het_han >= date.today(),
            )
            .order_by(HoSoPhapLy.ngay_het_han.asc())
            .limit(20)
        )
        rows = result.all()

    if not rows:
        return

    lines = [f"⚠️ *CẢNH BÁO: {len(rows)} hộ chiếu/visa sắp hết hạn*\n"]
    for doc, lao_dong in rows[:10]:
        con_lai = (doc.ngay_het_han - date.today()).days
        lines.append(
            f"• *{lao_dong.ho_ten}* — {doc.loai_giay_to.value} "
            f"hết hạn {doc.ngay_het_han} (còn {con_lai} ngày)"
        )

    msg = "\n".join(lines)
    nv_nb = await _get_nv_with_telegram(PhongBan.nhat_ban)
    nv_tv = await _get_nv_with_telegram(PhongBan.thuy_en_vien)
    await _broadcast(nv_nb + nv_tv, msg)


async def job_canh_bao_hop_dong() -> None:
    """Cảnh báo hợp đồng hết hạn trong 60 ngày lúc 7:30."""
    log.info("job_canh_bao_hop_dong")
    threshold = date.today() + timedelta(days=60)

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(HopDong)
            .where(
                HopDong.tinh_trang == TinhTrangHopDong.hieu_luc,
                HopDong.ngay_het_han <= threshold,
                HopDong.ngay_het_han >= date.today(),
            )
        )
        hd_list = result.scalars().all()

    if not hd_list:
        return

    msg = (
        f"📋 *CẢNH BÁO: {len(hd_list)} hợp đồng sắp hết hạn*\n"
        f"Trong vòng 60 ngày tới. Gõ `hợp đồng` để xem chi tiết."
    )
    nv_hc = await _get_nv_with_telegram(PhongBan.hanh_chinh)
    await _broadcast(nv_hc, msg)


async def job_kiem_tra_trinh_ky() -> None:
    """Kiểm tra và nhắc trình ký sắp quá hạn (mỗi 30 phút)."""
    log.info("job_kiem_tra_trinh_ky")
    tomorrow = date.today() + timedelta(days=1)

    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(TrinhKy, NhanVien)
            .join(NhanVien, TrinhKy.nguoi_duyet_id == NhanVien.id)
            .where(
                TrinhKy.tinh_trang == TinhTrangTrinhKy.cho_duyet,
                TrinhKy.han_duyet <= tomorrow,
                NhanVien.telegram_user_id.isnot(None),
            )
        )
        rows = result.all()

    for tk, approver in rows:
        msg = (
            f"⏰ *Nhắc phê duyệt văn bản*\n\n"
            f"📝 *{tk.ten_viec}*\n"
            f"⚠️ Hạn duyệt: *{tk.han_duyet.strftime('%d/%m/%Y %H:%M') if tk.han_duyet else 'Hết hạn'}*\n\n"
            f"Gõ `trình ký` để xem chi tiết."
        )
        try:
            await send_message(approver.telegram_user_id, msg)
        except Exception as exc:
            log.error("trinh_ky_notify_error", approver=approver.ho_ten, error=str(exc))


# ─── Setup scheduler ─────────────────────────────────────────────────

def setup_scheduler() -> AsyncIOScheduler:
    """Đăng ký tất cả jobs vào scheduler."""

    # Điểm danh 4 buổi / ngày
    for hour, minute, label in [
        (6, 15, "Buổi sáng sớm"),
        (8, 15, "Buổi sáng"),
        (13, 15, "Buổi chiều"),
        (19, 45, "Buổi tối"),
    ]:
        scheduler.add_job(
            job_diem_danh,
            CronTrigger(hour=hour, minute=minute),
            args=[label],
            id=f"diem_danh_{hour}_{minute}",
            replace_existing=True,
        )

    # Báo cáo tuần — thứ Sáu 16:00
    scheduler.add_job(
        job_bao_cao_tuan,
        CronTrigger(day_of_week="fri", hour=16, minute=0),
        id="bao_cao_tuan",
        replace_existing=True,
    )

    # Nhắc BHXH — ngày 20 hàng tháng 9:00
    scheduler.add_job(
        job_nhac_bhxh,
        CronTrigger(day=20, hour=9, minute=0),
        id="nhac_bhxh",
        replace_existing=True,
    )

    # Cảnh báo hộ chiếu — mỗi ngày 7:00
    scheduler.add_job(
        job_canh_bao_ho_chieu,
        CronTrigger(hour=7, minute=0),
        id="canh_bao_ho_chieu",
        replace_existing=True,
    )

    # Cảnh báo hợp đồng — mỗi ngày 7:30
    scheduler.add_job(
        job_canh_bao_hop_dong,
        CronTrigger(hour=7, minute=30),
        id="canh_bao_hop_dong",
        replace_existing=True,
    )

    # Kiểm tra trình ký — mỗi 30 phút
    scheduler.add_job(
        job_kiem_tra_trinh_ky,
        CronTrigger(minute="*/30"),
        id="kiem_tra_trinh_ky",
        replace_existing=True,
    )

    log.info("scheduler_setup", jobs=len(scheduler.get_jobs()))
    return scheduler
