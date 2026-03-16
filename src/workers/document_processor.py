"""
src/workers/document_processor.py — Quy trình xử lý tài liệu (OCR -> Embedding -> Qdrant)
"""
import io
import uuid
import structlog
from pdf2image import convert_from_bytes
from src.integrations import qwen_client, qdrant_client, xor_storage
from src.database import get_db, engine
from src.database.models import TaiLieu, TinhTrangTaiLieu
from sqlalchemy import update

log = structlog.get_logger(__name__)

async def process_document(object_name: str, metadata: dict):
    """
    Quy trình xử lý một tài liệu mới:
    1. Tải file từ CEPH.
    2. Nếu là PDF, chuyển thành ảnh.
    3. Gọi Qwen2.5-VL để lấy nội dung Markdown.
    4. Chia nhỏ văn bản (Chunking).
    5. Gọi Qwen3-Embedding để lấy vector.
    6. Lưu vào Qdrant với metadata.
    """
    doc_id = metadata.get("doc_id")
    
    async def update_status(status: TinhTrangTaiLieu = None, ocr_p: int = None, vec_p: int = None, error: str = None):
        if not doc_id: return
        async with engine.begin() as conn:
            values = {}
            if status: values["tinh_trang"] = status
            if ocr_p is not None: values["tien_do_ocr"] = ocr_p
            if vec_p is not None: values["tien_do_vector"] = vec_p
            if error: values["loi_nhan"] = error
            
            await conn.execute(
                update(TaiLieu).where(TaiLieu.id == doc_id).values(**values)
            )

    try:
        log.info("processing_document_start", object=object_name, doc_id=doc_id)
        await update_status(status=TinhTrangTaiLieu.dang_ocr, ocr_p=5)
        
        # 1. Download
        content = await xor_storage.storage.download_file(object_name)
        
        # 2. Convert to Images (nếu là PDF)
        # Giả định file PDF, xử lý trang đầu tiên làm ví dụ
        images = convert_from_bytes(content)
        
        full_markdown = ""
        for i, img in enumerate(images):
            # Lưu ảnh vào buffer để gửi qua API
            img_byte_arr = io.BytesIO()
            img.save(img_byte_arr, format='JPEG')
            img_bytes = img_byte_arr.getvalue()
            
            # 3. OCR với Qwen-VL
            log.info("ocr_page", page=i+1)
            page_text = await qwen_client.get_image_description(img_bytes)
            full_markdown += f"\n\n--- Page {i+1} ---\n\n" + page_text
            
            # Cập nhật tiến độ OCR
            progress = int(((i + 1) / len(images)) * 100)
            await update_status(ocr_p=progress)

        await update_status(status=TinhTrangTaiLieu.dang_vector_hoa, ocr_p=100)

        # 4. Chunking (Đơn giản hóa: cắt theo trang hoặc độ dài)
        # TODO: Implement thông minh hơn với RecursiveCharacterTextSplitter
        chunks = [full_markdown[i:i+2000] for i in range(0, len(full_markdown), 2000)]
        
        # 5 & 6. Embedding and Indexing
        points = []
        total_chunks = len(chunks)
        for idx, chunk in enumerate(chunks):
            vector = await qwen_client.get_embeddings(chunk)
            point_id = str(uuid.uuid4())

            # Payload bao gồm nội dung gốc và metadata để filter
            payload = {
                "content": chunk,
                "source": object_name,
                **metadata
            }

            points.append({
                "id": point_id,
                "vector": vector,
                "payload": payload
            })

            # Cập nhật tiến độ Vector
            v_progress = int(((idx + 1) / total_chunks) * 100)
            await update_status(vec_p=v_progress)
            
        await qdrant_client.upsert_points(points)
        await update_status(status=TinhTrangTaiLieu.hoan_thanh, vec_p=100)
        log.info("processing_document_complete", object=object_name, chunks=len(chunks))
        
    except Exception as exc:
        log.error("processing_document_failed", object=object_name, error=str(exc))
        await update_status(status=TinhTrangTaiLieu.loi, error=str(exc))
        raise
