"""
src/integrations/qwen_client.py — Qwen Vision & Embedding API Client
"""
import base64
import httpx
import structlog
from src.config import settings

import io
from PIL import Image

log = structlog.get_logger(__name__)

def optimize_image(image_bytes: bytes, max_size: int = 1500, quality: int = 80) -> bytes:
    """
    Nén và giảm độ phân giải ảnh để tiết kiệm Vision Tokens.
    - max_size: Kích thước cạnh dài nhất (pixel).
    - quality: Chất lượng nén JPEG.
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        
        # Giữ tỉ lệ khung hình
        if max(img.size) > max_size:
            ratio = max_size / max(img.size)
            new_size = (int(img.width * ratio), int(img.height * ratio))
            img = img.resize(new_size, Image.Resampling.LANCZOS)
            log.debug("image_resized", original=img.size, new=new_size)

        # Chuyển về RGB nếu cần (tránh lỗi nén JPEG với ảnh PNG alpha)
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")

        buffer = io.BytesIO()
        img.save(buffer, format="JPEG", quality=quality, optimize=True)
        optimized_bytes = buffer.getvalue()
        
        reduction = (1 - len(optimized_bytes) / len(image_bytes)) * 100
        log.info("image_optimized", original_kb=len(image_bytes)/1024, optimized_kb=len(optimized_bytes)/1024, reduction_pct=f"{reduction:.1f}%")
        
        return optimized_bytes
    except Exception as exc:
        log.error("image_optimization_failed", error=str(exc))
        return image_bytes

async def get_image_description(image_bytes: bytes, prompt: str = "Hãy mô tả chi tiết văn bản trong ảnh này, chuyển sang định dạng Markdown nếu có bảng biểu.") -> str:
    """
    Sử dụng Qwen2.5-VL-72B để OCR. Ảnh đã được tối ưu để tiết kiệm chi phí.
    """
    # Tối ưu ảnh trước khi gửi
    processed_image = optimize_image(image_bytes)
    encoded_image = base64.b64encode(processed_image).decode("utf-8")
    
    payload = {
        "model": settings.qwen_vl_model,
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}
                    }
                ]
            }
        ],
        "temperature": 0.1,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            resp = await client.post(
                f"{settings.qwen_api_base}/chat/completions",
                headers={"Authorization": f"Bearer {settings.qwen_api_key}"},
                json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"]
        except Exception as exc:
            log.error("qwen_vl_error", error=str(exc))
            raise

async def get_embeddings(text: str) -> list[float]:
    """
    Sử dụng Qwen3-Embedding-8B để lấy vector cho văn bản.
    """
    payload = {
        "model": settings.qwen_embed_model,
        "input": text,
    }

    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            resp = await client.post(
                f"{settings.qwen_api_base}/embeddings",
                headers={"Authorization": f"Bearer {settings.qwen_api_key}"},
                json=payload
            )
            resp.raise_for_status()
            data = resp.json()
            return data["data"][0]["embedding"]
        except Exception as exc:
            log.error("qwen_embedding_error", error=str(exc))
            raise
