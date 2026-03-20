"""
src/router.py — Message router: nhận Telegram Update → dispatch đến đúng xAI-CB agent
"""
import structlog
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.agents import (
    XCBPhapLy, XCBGiaoDuc, XCBBaoHiem, XCBTaiNguyen,
    XCBNongNghiep, XCBCongNghiep, XCBHanhChinh,
    XCBDoanhNghiep, XCBGiamSat
)
from src.database.models import CanBo, PhongBan
from src.integrations.telegram_bot import send_message, send_typing_action

log = structlog.get_logger(__name__)

# Khởi tạo 9 agent instances (stateless)
# Map theo PhongBan enum — dùng fallback hanh_chinh cho các phòng ban chưa map
_agents_by_id = {
    "pl":  XCBPhapLy(),
    "gd":  XCBGiaoDuc(),
    "bh":  XCBBaoHiem(),
    "tn":  XCBTaiNguyen(),
    "nn":  XCBNongNghiep(),
    "cn":  XCBCongNghiep(),
    "hc":  XCBHanhChinh(),
    "dn":  XCBDoanhNghiep(),
    "gm":  XCBGiamSat(),
}

# Giữ lại _agents dict để tương thích với api_router cũ (keyed by PhongBan)
_agents = {
    PhongBan.hanh_chinh: _agents_by_id["hc"],
    PhongBan.ke_toan:    _agents_by_id["hc"],
    PhongBan.lanh_dao:   _agents_by_id["gm"],
    PhongBan.tgd:        _agents_by_id["gm"],
    PhongBan.dao_tao:    _agents_by_id["gd"],
    PhongBan.nhat_ban:   _agents_by_id["dn"],
    PhongBan.thuy_en_vien: _agents_by_id["hc"],
    PhongBan.han_quoc:   _agents_by_id["dn"],
}

# Theo dõi update_id đã xử lý
_processed_updates: set[int] = set()
_MAX_DEDUP_SIZE = 10_000


async def route_update(update: dict, db: AsyncSession) -> None:
    """
    Nhận Telegram Update object, tìm CanBo, dispatch đến agent phù hợp.
    """
    update_id = update.get("update_id", 0)

    if update_id in _processed_updates:
        log.warning("duplicate_update", update_id=update_id)
        return
    _processed_updates.add(update_id)
    if len(_processed_updates) > _MAX_DEDUP_SIZE:
        _processed_updates.clear()

    message_obj = update.get("message") or update.get("edited_message")
    if not message_obj:
        return

    chat_id: int = message_obj["chat"]["id"]
    telegram_user_id: int = message_obj["from"]["id"]
    text: str = message_obj.get("text", "").strip()

    if not text:
        await send_message(chat_id, "⚠️ Vui lòng gửi tin nhắn dạng văn bản.")
        return

    result = await db.execute(
        select(CanBo).where(CanBo.telegram_user_id == telegram_user_id)
    )
    nhan_vien: CanBo | None = result.scalar_one_or_none()

    if not nhan_vien:
        await send_message(
            chat_id,
            "❌ Tài khoản Telegram của bạn chưa được liên kết với hệ thống xCB.\n"
            "Vui lòng liên hệ bộ phận quản trị để được hỗ trợ.",
        )
        return

    if not nhan_vien.dang_cong_tac:
        await send_message(chat_id, "⚠️ Tài khoản của bạn đã bị vô hiệu hoá.")
        return

    agent = _agents.get(nhan_vien.linh_vuc, _agents_by_id["hc"])
    await send_typing_action(chat_id)

    log.info(
        "routing",
        agent=agent.AGENT_ID,
        nhan_vien=nhan_vien.ho_ten,
        phong_ban=nhan_vien.linh_vuc.value,
        text_snippet=text[:80],
    )

    reply = await agent.handle(message=text, nhan_vien=nhan_vien, db=db)
    await send_message(chat_id, reply)
