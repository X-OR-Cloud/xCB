"""
src/api_router.py — REST API cho React Frontend của xCB Platform
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from src.database import get_db
from src.database.models import TaiLieu, TinhTrangTaiLieu, CanBo
from src.workers.document_processor import process_document

router = APIRouter(prefix="/api", tags=["Web-API"])

_ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

# ─── Dashboard Hành Chính Công ────────────────────────────────────────

@router.get("/dashboard/stats")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """Trả về các chỉ số hành chính công cho Dashboard xCB."""
    return {
        "ho_so_tiep_nhan": "1,284",
        "tiep_nhan_change": "+8.3%",
        "ti_le_dung_han": "94.2%",
        "dung_han_change": "+2.1%",
        "dang_cho": "187",
        "cho_change": "-5.4%",
        "qua_han": "23",
        "qua_han_change": "-12.0%",
    }

@router.get("/dashboard/risk-analysis")
async def get_risk_analysis():
    """Phân tích tỉ lệ hồ sơ theo từng lĩnh vực nghiệp vụ."""
    return [
        {"dept": "Đất đai - Tài nguyên",  "risk": 28},
        {"dept": "Bảo hiểm xã hội",        "risk": 22},
        {"dept": "Hành chính chung",        "risk": 18},
        {"dept": "Giáo dục - Đào tạo",     "risk": 15},
        {"dept": "Hỗ trợ Doanh nghiệp",    "risk": 12},
        {"dept": "Nông nghiệp",             "risk": 5},
    ]

@router.get("/dashboard/monthly-trend")
async def get_monthly_trend():
    """Xu hướng hồ sơ theo tháng (6 tháng gần nhất)."""
    return [
        {"month": "T10", "tiep_nhan": 980, "hoan_thanh": 940, "qua_han": 32},
        {"month": "T11", "tiep_nhan": 1050, "hoan_thanh": 1010, "qua_han": 28},
        {"month": "T12", "tiep_nhan": 890,  "hoan_thanh": 870,  "qua_han": 15},
        {"month": "T1",  "tiep_nhan": 1120, "hoan_thanh": 1080, "qua_han": 30},
        {"month": "T2",  "tiep_nhan": 1200, "hoan_thanh": 1150, "qua_han": 25},
        {"month": "T3",  "tiep_nhan": 1284, "hoan_thanh": 1205, "qua_han": 23},
    ]

@router.get("/dashboard/agents-status")
async def get_agents_status():
    """Trạng thái 9 xAI-CB agents."""
    return [
        {"id": "pl", "name": "xAI-PL", "desc": "Pháp Lý",              "status": "online", "queries_today": 142},
        {"id": "gd", "name": "xAI-GD", "desc": "Giáo Dục",             "status": "online", "queries_today": 98},
        {"id": "bh", "name": "xAI-BH", "desc": "Bảo Hiểm Xã Hội",     "status": "online", "queries_today": 215},
        {"id": "tn", "name": "xAI-TN", "desc": "Tài Nguyên - Đất Đai", "status": "online", "queries_today": 178},
        {"id": "nn", "name": "xAI-NN", "desc": "Nông Nghiệp",          "status": "away",   "queries_today": 64},
        {"id": "cn", "name": "xAI-CN", "desc": "Công Nghiệp",          "status": "online", "queries_today": 87},
        {"id": "hc", "name": "xAI-HC", "desc": "Hành Chính Công",      "status": "online", "queries_today": 310},
        {"id": "dn", "name": "xAI-DN", "desc": "Hỗ Trợ Doanh Nghiệp", "status": "online", "queries_today": 123},
        {"id": "gm", "name": "xAI-GM", "desc": "Giám Sát Hệ Thống",   "status": "online", "queries_today": 45},
    ]

# ─── Data Manager API (GIỮ NGUYÊN) ───────────────────────────────────

@router.get("/data/files")
async def get_data_files(db: AsyncSession = Depends(get_db)):
    """Lấy danh sách tệp tin đang xử lý."""
    result = await db.execute(select(TaiLieu).order_by(TaiLieu.ngay_tao.desc()).limit(20))
    files = result.scalars().all()
    return files

@router.post("/data/upload")
async def upload_document(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    linh_vuc: str = Form("hanh_chinh"),
    db: AsyncSession = Depends(get_db)
):
    """Tải lên tài liệu và bắt đầu xử lý OCR + Vector."""
    from src.integrations.xor_storage import storage

    if file.content_type not in _ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Loại file không được hỗ trợ: {file.content_type}. Chỉ chấp nhận PDF và Word.",
        )

    db_file = TaiLieu(
        ten_file=file.filename,
        loai_file=file.filename.split(".")[-1],
        tinh_trang=TinhTrangTaiLieu.cho_xu_ly
    )
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)

    content = await file.read()
    object_name = f"docs/{linh_vuc}/{db_file.id}_{uuid.uuid4().hex[:8]}_{file.filename}"
    db_file.duong_dan_storage = object_name
    db_file.dung_luong = len(content)
    await db.commit()

    await storage.upload_file(content, object_name, file.content_type)
    metadata = {"doc_id": db_file.id, "linh_vuc": linh_vuc}
    background_tasks.add_task(process_document, object_name, metadata)

    return db_file

# ─── Knowledge Base API ───────────────────────────────────────────────

@router.get("/kb/collections")
async def get_kb_collections():
    """9 bộ sưu tập tri thức xCB theo lĩnh vực nghiệp vụ."""
    return [
        {"id": "phap_luat",     "name": "Pháp Luật",              "docs": 2450, "updated": "10p trước",  "status": "RAG HOẠT ĐỘNG", "health": 97, "color": "indigo"},
        {"id": "bao_hiem",      "name": "Bảo Hiểm Xã Hội",       "docs": 1820, "updated": "30p trước",  "status": "MẬT ĐỘ CAO",   "health": 95, "color": "green"},
        {"id": "dat_dai",       "name": "Tài Nguyên - Đất Đai",   "docs": 1640, "updated": "1g trước",   "status": "RAG HOẠT ĐỘNG", "health": 92, "color": "teal"},
        {"id": "hanh_chinh",    "name": "Hành Chính Công",        "docs": 3100, "updated": "5p trước",   "status": "MẬT ĐỘ CAO",   "health": 98, "color": "blue"},
        {"id": "giao_duc",      "name": "Giáo Dục - Đào Tạo",    "docs": 980,  "updated": "2g trước",   "status": "RAG HOẠT ĐỘNG", "health": 88, "color": "amber"},
        {"id": "nong_nghiep",   "name": "Nông Nghiệp",            "docs": 720,  "updated": "Hôm qua",    "status": "ĐANG XỬ LÝ",   "health": 74, "color": "lime"},
        {"id": "cong_nghiep",   "name": "Công Nghiệp",            "docs": 850,  "updated": "3g trước",   "status": "RAG HOẠT ĐỘNG", "health": 89, "color": "orange"},
        {"id": "doanh_nghiep",  "name": "Hỗ Trợ Doanh Nghiệp",  "docs": 1120, "updated": "45p trước",  "status": "RAG HOẠT ĐỘNG", "health": 93, "color": "purple"},
        {"id": "giam_sat",      "name": "Giám Sát & Tổng Hợp",   "docs": 560,  "updated": "15p trước",  "status": "MẬT ĐỘ CAO",   "health": 96, "color": "cyan"},
    ]

@router.post("/kb/search")
async def kb_search(query: str, collection: str = "hanh_chinh"):
    """Tìm kiếm ngữ nghĩa trong kho tri thức xCB."""
    from src.integrations import qwen_client, qdrant_client
    vector = await qwen_client.get_embeddings(query)
    results = await qdrant_client.search_knowledge(vector, limit=3)
    return [
        {
            "filename": r.payload.get("original_filename", "Unknown"),
            "content": r.payload.get("content", ""),
            "score": r.score
        } for r in results
    ]

# ─── Agent Chat API ───────────────────────────────────────────────────

@router.post("/chat/{agent_id}")
async def agent_chat(agent_id: str, message: str, db: AsyncSession = Depends(get_db)):
    """Chat trực tiếp với xAI-CB Agent qua Web."""
    from src.router import _agents_by_id

    result = await db.execute(
        select(CanBo).where(CanBo.linh_vuc == "hanh_chinh").limit(1)
    )
    nhan_vien = result.scalar_one_or_none()

    if not nhan_vien:
        # Tạo CanBo giả để test khi chưa có DB
        class MockCanBo:
            id = 0
            ho_ten = "Quản trị viên xCB"
            linh_vuc = "hanh_chinh"
            telegram_user_id = 0
        nhan_vien = MockCanBo()

    agent = _agents_by_id.get(agent_id)
    if not agent:
        raise HTTPException(status_code=404, detail=f"Agent '{agent_id}' không tồn tại.")

    reply = await agent.handle(message=message, nhan_vien=nhan_vien, db=db)
    return {"reply": reply}
