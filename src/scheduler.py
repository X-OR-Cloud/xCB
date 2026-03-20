"""
src/scheduler.py — APScheduler: các tác vụ tự động (nhắc nhở, báo cáo)
Lưu ý: Các job gốc từ xHR phụ thuộc vào NhanVien, HopDong, LaoDong, TrinhKy, etc.
đã được stub/comment out. Chỉ giữ lại các job tương thích với xCB (CanBo, HoSoHanhChinh).
"""
from datetime import date, timedelta

import structlog
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy import func, select

from src.database.session import AsyncSessionLocal
from src.database.models import (
    CanBo, HoSoHanhChinh, TrangThaiHoSo, PhongBan,
)
from src.integrations.telegram_bot import send_message

log = structlog.get_logger(__name__)

VN_TIMEZONE = "Asia/Ho_Chi_Minh"
scheduler = AsyncIOScheduler(timezone=VN_TIMEZONE)


# ─── Helpers ─────────────────────────────────────────────────────────

async def _get_cb_with_telegram(linh_vuc: PhongBan | None = None) -> list[CanBo]:
    """Lấy danh sách cán bộ có telegram_user_id."""
    async with AsyncSessionLocal() as db:
        query = select(CanBo).where(
            CanBo.dang_cong_tac.is_(True),
            CanBo.telegram_user_id.isnot(None),
        )
        if linh_vuc:
            query = query.where(CanBo.linh_vuc == linh_vuc)
        result = await db.execute(query)
        return result.scalars().all()


async def _broadcast(can_bos: list[CanBo], message: str) -> None:
    """Gửi message đến nhiều cán bộ."""
    for cb in can_bos:
        try:
            await send_message(cb.telegram_user_id, message)
        except Exception as exc:
            log.error("broadcast_error", can_bo=cb.ho_ten, error=str(exc))


# ─── Job handlers ─────────────────────────────────────────────────────

async def job_diem_danh(session_label: str) -> None:
    """Nhắc điểm danh (6:15, 8:15, 13:15, 19:45)."""
    log.info("job_diem_danh", session=session_label)
    cb_dao_tao = await _get_cb_with_telegram(PhongBan.dao_tao)
    msg = (
        f"📋 *Nhắc điểm danh — {session_label}*\n"
        f"Vui lòng cập nhật điểm danh cho buổi này.\n"
        f"Gõ: `điểm danh` để xem danh sách."
    )
    await _broadcast(cb_dao_tao, msg)


async def job_bao_cao_tuan() -> None:
    """Báo cáo tuần gửi mỗi thứ Sáu 16:00."""
    log.info("job_bao_cao_tuan")
    async with AsyncSessionLocal() as db:
        tong_hs = await db.scalar(select(func.count(HoSoHanhChinh.id))) or 0
        dang_xu_ly = await db.scalar(
            select(func.count(HoSoHanhChinh.id)).where(
                HoSoHanhChinh.trang_thai == TrangThaiHoSo.dang_xu_ly
            )
        ) or 0
        qua_han = await db.scalar(
            select(func.count(HoSoHanhChinh.id)).where(
                HoSoHanhChinh.trang_thai == TrangThaiHoSo.qua_han
            )
        ) or 0

    msg = (
        f"📊 *BÁO CÁO TUẦN — {date.today().strftime('%d/%m/%Y')}*\n"
        f"{'─' * 30}\n"
        f"• Tổng hồ sơ hành chính: *{tong_hs}*\n"
        f"• Đang xử lý: *{dang_xu_ly}*\n"
        f"• Quá hạn: *{qua_han}*\n\n"
        f"Gõ `dashboard` để xem chi tiết đầy đủ."
    )
    # Gửi cho lãnh đạo
    cb_lanh_dao = await _get_cb_with_telegram(PhongBan.lanh_dao)
    cb_tgd = await _get_cb_with_telegram(PhongBan.tgd)
    await _broadcast(cb_lanh_dao + cb_tgd, msg)


async def job_nhac_bhxh() -> None:
    """Nhắc đóng BHXH ngày 20 hàng tháng lúc 9:00."""
    log.info("job_nhac_bhxh")
    async with AsyncSessionLocal() as db:
        tong_cb = await db.scalar(
            select(func.count(CanBo.id)).where(CanBo.dang_cong_tac.is_(True))
        ) or 0

    msg = (
        f"🏦 *NHẮC ĐÓNG BHXH THÁNG {date.today().month}*\n\n"
        f"Hạn đóng: *ngày 20/{date.today().month}/{date.today().year}*\n"
        f"Tổng cán bộ cần đóng: *{tong_cb}*\n\n"
        f"Phòng Kế toán vui lòng chuẩn bị danh sách và chứng từ."
    )
    cb_ke_toan = await _get_cb_with_telegram(PhongBan.ke_toan)
    cb_hanh_chinh = await _get_cb_with_telegram(PhongBan.hanh_chinh)
    await _broadcast(cb_ke_toan + cb_hanh_chinh, msg)


# NOTE: job_canh_bao_ho_chieu — disabled (requires HoSoPhapLy, LaoDong, LoaiGiayTo from xHR)
# NOTE: job_canh_bao_hop_dong — disabled (requires HopDong, LaoDong from xHR)
# NOTE: job_kiem_tra_trinh_ky — disabled (requires TrinhKy, NhanVien from xHR)


async def job_canh_bao_ho_so_qua_han() -> None:
    """Cảnh báo hồ sơ hành chính quá hạn hoặc sắp quá hạn — mỗi ngày 7:00."""
    log.info("job_canh_bao_ho_so_qua_han")
    today = date.today()
    threshold = today + timedelta(days=3)

    async with AsyncSessionLocal() as db:
        qua_han = await db.scalar(
            select(func.count(HoSoHanhChinh.id)).where(
                HoSoHanhChinh.trang_thai == TrangThaiHoSo.qua_han
            )
        ) or 0
        sap_het_han = await db.scalar(
            select(func.count(HoSoHanhChinh.id)).where(
                HoSoHanhChinh.trang_thai == TrangThaiHoSo.dang_xu_ly,
                HoSoHanhChinh.han_tra_ket_qua <= threshold,
                HoSoHanhChinh.han_tra_ket_qua >= today,
            )
        ) or 0

    if not qua_han and not sap_het_han:
        return

    msg = (
        f"⚠️ *CẢNH BÁO HỒ SƠ — {today.strftime('%d/%m/%Y')}*\n\n"
        f"• Hồ sơ quá hạn: *{qua_han}*\n"
        f"• Sắp hết hạn (≤ 3 ngày): *{sap_het_han}*\n\n"
        f"Vui lòng kiểm tra và xử lý kịp thời."
    )
    cb_hanh_chinh = await _get_cb_with_telegram(PhongBan.hanh_chinh)
    cb_lanh_dao = await _get_cb_with_telegram(PhongBan.lanh_dao)
    await _broadcast(cb_hanh_chinh + cb_lanh_dao, msg)


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

    # Cảnh báo hồ sơ quá hạn — mỗi ngày 7:00
    scheduler.add_job(
        job_canh_bao_ho_so_qua_han,
        CronTrigger(hour=7, minute=0),
        id="canh_bao_ho_so_qua_han",
        replace_existing=True,
    )

    log.info("scheduler_setup", jobs=len(scheduler.get_jobs()))
    return scheduler
