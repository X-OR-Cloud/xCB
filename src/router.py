"""
src/router.py — Message router: nhận Telegram Update → dispatch đến đúng MOLTY agent
"""
import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents import MoltyCEO, MoltyDT, MoltyHC, MoltyNB, MoltyTV
from src.database.models import NhanVien, PhongBan
from src.integrations.telegram_bot import send_message, send_typing_action

log = structlog.get_logger(__name__)

# Khởi tạo 5 agent instances (stateless)
_agents = {
    PhongBan.nhat_ban:   MoltyNB(),
    PhongBan.thuy_en_vien: MoltyTV(),
    PhongBan.han_quoc:   MoltyTV(),
    PhongBan.dao_tao:    MoltyDT(),
    PhongBan.hanh_chinh: MoltyHC(),
    PhongBan.ke_toan:    MoltyHC(),
    PhongBan.lanh_dao:   MoltyCEO(),
    PhongBan.tgd:        MoltyCEO(),
}

# Theo dõi update_id đã xử lý (in-memory dedup — đủ dùng với 1 instance)
_processed_updates: set[int] = set()
_MAX_DEDUP_SIZE = 10_000


async def route_update(update: dict, db: AsyncSession) -> None:
    """
    Nhận Telegram Update object, tìm NhanVien, dispatch đến agent phù hợp.
    """
    update_id = update.get("update_id", 0)

    # ── Deduplication ───────────────────────────────────────────────
    if update_id in _processed_updates:
        log.warning("duplicate_update", update_id=update_id)
        return
    _processed_updates.add(update_id)
    if len(_processed_updates) > _MAX_DEDUP_SIZE:
        _processed_updates.clear()

    # ── Lấy message ─────────────────────────────────────────────────
    message_obj = update.get("message") or update.get("edited_message")
    if not message_obj:
        log.debug("no_message_in_update", update_id=update_id)
        return

    chat_id: int = message_obj["chat"]["id"]
    telegram_user_id: int = message_obj["from"]["id"]
    text: str = message_obj.get("text", "").strip()

    if not text:
        await send_message(chat_id, "⚠️ Vui lòng gửi tin nhắn dạng văn bản.")
        return

    # ── Tra cứu nhân viên ───────────────────────────────────────────
    result = await db.execute(
        select(NhanVien).where(NhanVien.telegram_user_id == telegram_user_id)
    )
    nhan_vien: NhanVien | None = result.scalar_one_or_none()

    if not nhan_vien:
        log.warning("unknown_telegram_user", telegram_user_id=telegram_user_id)
        await send_message(
            chat_id,
            "❌ Tài khoản Telegram của bạn chưa được liên kết với hệ thống xHR.\n"
            "Vui lòng liên hệ phòng Hành chính để được hỗ trợ.",
        )
        return

    if not nhan_vien.dang_lam_viec:
        await send_message(chat_id, "⚠️ Tài khoản của bạn đã bị vô hiệu hoá.")
        return

    # ── Dispatch đến agent ──────────────────────────────────────────
    agent = _agents.get(nhan_vien.phong_ban)
    if not agent:
        log.error("no_agent_for_phong_ban", phong_ban=nhan_vien.phong_ban)
        await send_message(chat_id, "⚠️ Phòng ban chưa được cấu hình agent. Liên hệ admin.")
        return

    # Hiển thị typing indicator
    await send_typing_action(chat_id)

    log.info(
        "routing",
        agent=agent.AGENT_ID,
        nhan_vien=nhan_vien.ho_ten,
        phong_ban=nhan_vien.phong_ban.value,
        text_snippet=text[:80],
    )

    reply = await agent.handle(message=text, nhan_vien=nhan_vien, db=db)
    await send_message(chat_id, reply)
