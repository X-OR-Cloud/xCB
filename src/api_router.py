"""
src/api_router.py — REST API cho React Frontend của xHR
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
import uuid

from src.database import get_db
from src.database.models import (
    TaiLieu, TinhTrangTaiLieu, PhongBan, 
    LaoDong, HopDong, TinhTrangHopDong,
    AuditLog
)
from src.workers.document_processor import process_document

router = APIRouter(prefix="/api", tags=["Web-API"])

_ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

# --- Dashboard API ---

@router.get("/dashboard/stats")
async def get_dashboard_stats(db: AsyncSession = Depends(get_db)):
    """Trả về các chỉ số chính cho CEO Dashboard."""
    # Mock data dựa trên mockup, sau này query thực tế từ DB
    return {
        "revenue_ytd": "$128.5M",
        "revenue_change": "+12.5%",
        "margin": "24.2%",
        "margin_change": "+3.1%",
        "risk_index": "Thấp",
        "risk_change": "-0.5%",
        "goal_completion": "88%",
        "goal_change": "+2.0%"
    }

@router.get("/dashboard/risk-analysis")
async def get_risk_analysis():
    """Phân tích rủi ro theo phòng ban."""
    return [
        {"dept": "Vận hành", "risk": 12},
        {"dept": "Tài chính", "risk": 17},
        {"dept": "Nhân sự", "risk": 22},
        {"dept": "Cung ứng", "risk": 27}
    ]

# --- Data Manager API ---

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
    phong_ban: str = Form("hanh_chinh"),
    db: AsyncSession = Depends(get_db)
):
    """Tải lên tài liệu và bắt đầu xử lý."""
    from src.integrations.xor_storage import storage

    # 0. Validate MIME type
    if file.content_type not in _ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Loại file không được hỗ trợ: {file.content_type}. Chỉ chấp nhận PDF và Word.",
        )

    # 1. Tạo bản ghi DB
    db_file = TaiLieu(
        ten_file=file.filename,
        loai_file=file.filename.split(".")[-1],
        phong_ban=phong_ban,
        tinh_trang=TinhTrangTaiLieu.cho_xu_ly
    )
    db.add(db_file)
    await db.commit()
    await db.refresh(db_file)

    content = await file.read()
    object_name = f"docs/{db_file.id}_{uuid.uuid4().hex[:8]}_{file.filename}"
    db_file.duong_dan_storage = object_name
    db_file.dung_luong = len(content)
    await db.commit()

    # 2. Upload storage
    await storage.upload_file(content, object_name, file.content_type)

    # 3. Kích hoạt Worker
    metadata = {"doc_id": db_file.id, "phong_ban": phong_ban}
    background_tasks.add_task(process_document, object_name, metadata)

    return db_file

# --- Knowledge Base API ---

@router.get("/kb/collections")
async def get_kb_collections():
    """Thông tin các bộ sưu tập tri thức."""
    return [
        {
            "id": "nhat_ban",
            "name": "Thị trường Nhật Bản",
            "docs": 1200,
            "updated": "5p trước",
            "status": "MẬT ĐỘ CAO",
            "health": 95
        },
        {
            "id": "thuy_en_vien",
            "name": "Quản lý Thuyền viên",
            "docs": 850,
            "updated": "1g trước",
            "status": "RAG HOẠT ĐỘNG",
            "health": 88
        }
    ]

@router.post("/kb/search")
async def kb_search(query: str, collection: str = "xhr_knowledge"):
    """Tìm kiếm ngữ nghĩa (Semantic Search)."""
    from src.integrations import qwen_client, qdrant_client
    
    # 1. Vector hóa query
    vector = await qwen_client.get_embeddings(query)
    
    # 2. Tìm trong Qdrant
    results = await qdrant_client.search_knowledge(vector, limit=3)
    
    return [
        {
            "filename": r.payload.get("original_filename", "Unknown"),
            "content": r.payload.get("content", ""),
            "score": r.score
        } for r in results
    ]

# --- Agent Interaction API ---

@router.post("/chat/{agent_id}")
async def agent_chat(agent_id: str, message: str, db: AsyncSession = Depends(get_db)):
    """Chat trực tiếp với Agent qua Web."""
    from src.router import _agents
    from src.database.models import NhanVien
    
    # Lấy nhan_vien giả định (admin cho web)
    # Trong thực tế sẽ lấy từ JWT token của user đang đăng nhập
    result = await db.execute(select(NhanVien).where(NhanVien.phong_ban == "lanh_dao").limit(1))
    nhan_vien = result.scalar_one_or_none()
    
    if not nhan_vien:
        raise HTTPException(status_code=404, detail="Không tìm thấy profile nhân viên phù hợp.")

    # Tìm agent tương ứng
    # agent_id có thể là 'nb', 'tv', 'hc', 'ceo' ...
    agent_map = {
        'nb': 'nhat_ban',
        'tv': 'thuy_en_vien',
        'hc': 'hanh_chinh',
        'ceo': 'lanh_dao'
    }
    pb_key = agent_map.get(agent_id)
    agent = _agents.get(pb_key)
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent không tồn tại.")

    reply = await agent.handle(message=message, nhan_vien=nhan_vien, db=db)
    
    return {"reply": reply}
