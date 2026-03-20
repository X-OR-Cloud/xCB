"""
src/skills/rag_base.py — Các hàm bổ trợ RAG (Retrieval-Augmented Generation) cho Agents
"""
import structlog
from src.integrations import qwen_client, qdrant_client
from src.database.models import CanBo

log = structlog.get_logger(__name__)

async def search_knowledge_base(query: str, nhan_vien: CanBo, limit: int = 3) -> str:
    """
    Tìm kiếm thông tin từ kiến thức đã index trong Qdrant.
    Có thể lọc theo phòng ban để đảm bảo bảo mật dữ liệu.
    """
    try:
        # 1. Thu thập vector cho câu hỏi
        query_vector = await qwen_client.get_embeddings(query)
        
        # 2. Định nghĩa filter dựa trên quyền của nhân viên
        # Lãnh đạo / TGD có thể xem tất cả; các phòng ban khác chỉ xem tài liệu của mình
        filter_dict = {}
        if nhan_vien.linh_vuc.value not in ["lanh_dao", "tgd"]:
            filter_dict["phong_ban"] = nhan_vien.linh_vuc.value

        # 3. Search Qdrant
        results = await qdrant_client.search_knowledge(
            query_vector=query_vector,
            limit=limit,
            filter_dict=filter_dict
        )
        
        if not results:
            return ""
            
        # 4. Gom nội dung
        context_lines = []
        for res in results:
            content = res.payload.get("content", "")
            source = res.payload.get("source", "Tài liệu")
            context_lines.append(f"--- Từ: {source} ---\n{content}")
            
        return "\n\n".join(context_lines)
        
    except Exception as exc:
        log.error("rag_search_error", query=query, error=str(exc))
        return ""

async def generate_rag_answer(agent_system_prompt: str, user_message: str, context: str) -> str:
    """
    Gửi prompt và ngữ cảnh tìm được cho Claude để sinh câu trả lời.
    """
    from src.integrations.claude_client import ask_claude
    
    rag_prompt = (
        f"{agent_system_prompt}\n\n"
        "Dưới đây là một số thông tin từ tài liệu nội bộ (Knowledge Base) có liên quan đến câu hỏi của người dùng. "
        "Hãy dựa vào thông tin này để trả lời một cách chính xác nhất. Nếu thông tin không có trong tài liệu, "
        "hãy trả lời dựa trên kiến thức của bạn và ghi chú rõ điều đó.\n\n"
        "NGỮ CẢNH TÀI LIỆU:\n"
        f"{context}\n\n"
        "CÂU HỎI NGƯỜI DÙNG:"
    )
    
    return await ask_claude(system_prompt=rag_prompt, user_message=user_message)
