"""
src/integrations/qdrant_client.py — Qdrant Vector DB integration for xHR
"""
import structlog
from qdrant_client import QdrantClient, AsyncQdrantClient
from qdrant_client.http import models

from src.config import settings

log = structlog.get_logger(__name__)

_client = AsyncQdrantClient(
    url=settings.qdrant_url,
    api_key=settings.qdrant_api_key
)

COLLECTION_NAME = "xhr_knowledge"

async def init_qdrant():
    """Khởi tạo collection nếu chưa tồn tại."""
    try:
        collections = await _client.get_collections()
        exists = any(c.name == COLLECTION_NAME for c in collections.collections)
        
        if not exists:
            # Qwen3-Embedding-8B thường có output dimension là 1536 hoặc 4096 
            # (Giả định 1536 cho model này, có thể điều chỉnh sau)
            await _client.create_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=models.VectorParams(
                    size=1536, 
                    distance=models.Distance.COSINE
                ),
            )
            log.info("qdrant_collection_created", name=COLLECTION_NAME)
    except Exception as exc:
        log.error("qdrant_init_error", error=str(exc))

async def upsert_points(points: list[dict]):
    """
    Thêm dữ liệu vào Qdrant.
    points: list[{id, vector, payload}]
    """
    try:
        await _client.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                models.PointStruct(
                    id=p["id"],
                    vector=p["vector"],
                    payload=p["payload"]
                ) for p in points
            ]
        )
        log.info("qdrant_upsert_success", count=len(points))
    except Exception as exc:
        log.error("qdrant_upsert_error", error=str(exc))
        raise

async def search_knowledge(
    query_vector: list[float], 
    limit: int = 5, 
    filter_dict: dict | None = None
):
    """Tìm kiếm ngữ cảnh liên quan."""
    search_filter = None
    if filter_dict:
        conditions = [
            models.FieldCondition(
                key=k,
                match=models.MatchValue(value=v)
            ) for k, v in filter_dict.items()
        ]
        search_filter = models.Filter(must=conditions)

    try:
        results = await _client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            limit=limit,
            query_filter=search_filter
        )
        return results
    except Exception as exc:
        log.error("qdrant_search_error", error=str(exc))
        return []
