<div align="center">
 
 # 🤖 xHR — AI-native HR Platform
 
 **Nền tảng quản lý nhân sự thông minh nâng cường RAG cho Thinh Long Group**
 
 [![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
 [![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
 [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
 [![Claude AI](https://img.shields.io/badge/Claude-Anthropic-D97706?style=for-the-badge&logo=anthropic&logoColor=white)](https://anthropic.com)
 [![Qdrant](https://img.shields.io/badge/Qdrant-Vector_DB-ff4b4b?style=for-the-badge&logo=qdrant&logoColor=white)](https://qdrant.tech)
 [![Telegram](https://img.shields.io/badge/Telegram-Bot_API-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots)
 
 > **5 AI agents chuyên biệt** — tự động hoá quy trình HR và quản lý tri thức (RAG) thông qua Telegram Bot, tích hợp sâu với **Qwen Vision & Embedding** và **Qdrant Vector DB**.
 
 </div>
 
 ---
 
 ## 📋 Mục lục
 
 - [Tổng quan](#-tổng-quan)
 - [Kiến trúc hệ thống RAG](#-kiến-trúc-hệ-thống-rag)
 - [AI Stack & Công nghệ](#-ai-stack--công-nghệ)
 - [5 MOLTY Agents](#-5-molty-agents)
 - [Tính năng nâng cao](#-tính-năng-nâng-cao)
 - [Cài đặt & Chạy](#-cài-đặt--chạy)
 - [API Endpoints](#-api-endpoints)
 - [Kết cấu tri thức (RAG Flow)](#-kết-cấu-tri-thức-rag-flow)
 
 ---
 
 ## 🎯 Tổng quan
 
 **xHR** không chỉ là một công cụ quản lý nhân sự (ERP) mà còn là một **Trợ lý tri thức**. Hệ thống có khả năng "đọc" và "hiểu" các tài liệu không cấu trúc như Hợp đồng PDF, Đơn hàng tuyển dụng Word, và Chứng từ tài chính ảnh để hỗ trợ nhân viên ra quyết định tức thì qua Telegram.
 
 ---
 
 ## 🏗 Kiến trúc hệ thống RAG
 
 ```mermaid
 graph TD
     A[Telegram / Admin] -->|Tài liệu PDF/Word/Ảnh| B[FastAPI Admin Route]
     B -->|Lưu trữ| C[X-OR CLOUD - CEPH Storage]
     C -->|Trigger| D[Worker Processor]
     
     subgraph AI_Inference
         D -->|Page Images| E[[Qwen2.5-VL-72B OCR]]
         E -->|Markdown| F[Chunking]
         F -->|Chunks| G[[Qwen3-Embedding-8B]]
     end
     
     G -->|Vectors| H[(Qdrant Vector DB)]
     
     I[User Telegram] -->|Hỏi về hợp đồng/đơn hàng| J[Agent Router]
     J -->|Search| H
     H -->|Ngữ cảnh| K[Claude AI]
     K -->|Trả lời thông minh| I
 ```
 
 ---
 
 ## 🤖 AI Stack & Công nghệ
 
 | Thành phần | Công nghệ sử dụng | Vai trò |
 |---|---|---|
 | **OCR & Vision** | `Qwen2.5-VL-72B-Instruct` | Đọc tài liệu ảnh/PDF, giữ cấu trúc Table/Markdown |
 | **Embedding** | `Qwen3-Embedding-8B` | Chuyển đổi văn bản tiếng Việt sang không gian Vector |
 | **Vector Search** | `Qdrant DB` | Lưu trữ và tìm kiếm ngữ cảnh tài liệu cực nhanh |
 | **Reasoning** | `Anthropic Claude 3.5 Sonnet` | Tư duy, phân loại intent và trả lời người dùng |
 | **Object Storage** | `X-OR CLOUD (CEPH)` | Lưu trữ tệp tin gốc ổn định, chuẩn S3 |
 
 ---
 
 ## ✨ Tính năng nâng cao
 
 - ✅ **RAG-Powered Conversations**: Agent tự tìm kiếm trong kho quy trình, hợp đồng để trả lời câu hỏi.
 - ✅ **Vision OCR**: Tự động bóc tách dữ liệu từ chứng từ kế toán, hộ chiếu qua ảnh chụp.
 - ✅ **Multi-agent Routing**: Tự động điều phối tin nhắn theo chuyên môn phòng ban.
 - ✅ **Automated Workflows**: Nhắc điểm danh, cảnh báo hộ chiếu hết hạn, nhắc đóng BHXH tự động.
 - ✅ **Audit Logging**: Ghi lại mọi hành động của AI agent để đối soát.
 
 ---
 
 ## 🚀 Cài đặt & Chạy
 
 ### 1. Cấu hình .env
 ```env
 # Core
 ANTHROPIC_API_KEY=sk-ant-...
 TELEGRAM_BOT_TOKEN=...
 
 # Storage (X-OR CLOUD)
 XOR_ACCESS_KEY=...
 XOR_SECRET_KEY=...
 XOR_ENDPOINT_URL=https://s3.x-or.cloud
 
 # Vector DB
 QDRANT_URL=http://qdrant:6333
 
 # Qwen API
 QWEN_API_BASE=...
 QWEN_API_KEY=...
 ```
 
 ### 2. Khởi động với Docker
 ```bash
 docker-compose up -d --build
 # Qdrant sẽ được khởi tạo tại localhost:6333
 # FastAPI Web docs tại localhost:8000/docs
 ```
 
 ---
 
 ## 🔌 API Endpoints (Mới)
 
 | Method | Endpoint | Mô tả |
 |---|---|---|
 | `POST` | `/admin/upload-document` | Upload PDF/Word để đưa vào kho tri thức |
 | `GET` | `/health` | Kiểm tra sức khỏe App & DB |
 | `POST` | `/webhook/telegram` | Cổng tiếp nhận tin nhắn từ Telegram |
 
 ---
 
 ## ⏰ Kết cấu tri thức (RAG Flow)
 
 1. **Capture**: Tài liệu được đẩy lên qua Admin API hoặc Telegram.
 2. **Refine**: Qwen-VL chuyển đổi PDF sang dạng Markdown để AI dễ hiểu bảng biểu.
 3. **Index**: Qwen3-Embedding tạo "dấu vân tay" vector cho từng đoạn văn bản và lưu vào Qdrant.
 4. **Retrieve**: Khi có câu hỏi, hệ thống tìm 3 đoạn văn liên quan nhất để làm ngữ cảnh.
 5. **Answer**: Claude tổng hợp ngữ cảnh và trả lời người dùng một cách tự nhiên bằng tiếng Việt.
 
 ---
 
 <div align="center">
 
 **Built with ❤️ for Thinh Long Group**
 
 *Powered by [Qwen AI](https://github.com/QwenLM/Qwen) · [Anthropic Claude](https://anthropic.com) · [Qdrant](https://qdrant.tech)*
 
 </div>
