"""
src/integrations/qwen_client.py — Qwen Vision & Embedding API Client
"""
import base64
import httpx
import structlog
from src.config import settings

log = structlog.get_logger(__name__)

async def get_image_description(image_bytes: bytes, prompt: str = "Hãy mô tả chi tiết văn bản trong ảnh này, chuyển sang định dạng Markdown nếu có bảng biểu.") -> str:
    """
    Sử dụng Qwen2.5-VL-72B để OCR và nhận diện văn bản.
    """
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")
    
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
