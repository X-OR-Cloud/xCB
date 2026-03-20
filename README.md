# xCB: Nền tảng Đa Tác nhân AI cho Công chức Địa phương

![xCB Logo](/logo.png)

**xCB** (x-Cloud Bureau) là hệ thống đa tác nhân AI kết hợp lưu trữ dữ liệu tri thức, được thiết kế chuyên biệt để hỗ trợ cán bộ công chức cấp Tỉnh, Huyện, Xã trong việc nâng cao kỹ năng nghiệp vụ và tối ưu hóa quy trình hành chính công.

---

## 🌟 Tính năng Cốt lõi

- **Hệ sinh thái 9 xAI-CB Agents**: Mỗi Agent được huấn luyện chuyên sâu cho từng lĩnh vực nghiệp vụ.
- **RAG (Retrieval-Augmented Generation)**: Truy xuất thông tin chính xác từ kho văn bản pháp luật, nghị định, thông tư của địa phương.
- **Trung tâm Nạp dữ liệu**: Hỗ trợ OCR và Vector hóa các tài liệu hành chính, hồ sơ công việc.
- **Dashboard Điều hành**: Giám sát thời gian thực tỉ lệ xử lý hồ sơ, hiệu suất cán bộ và cảnh báo rủi ro quá hạn.
- **Bản đồ Hiệu suất**: Trực quan hóa dữ liệu hành chính theo từng địa bàn quản lý.

## 🤖 Danh sách AI Agents (xAI-CB)

1.  **xAI-PL (Pháp lý)**: Tra cứu quy định, nghị định và tư vấn pháp luật.
2.  **xAI-GD (Giáo dục)**: Hỗ trợ quản lý giáo dục và đào tạo.
3.  **xAI-BH (Bảo hiểm)**: Giải đáp chính sách BHXH, BHYT.
4.  **xAI-TN (Tài nguyên)**: Nghiệp vụ Đất đai, Môi trường.
5.  **xAI-NN (Nông nghiệp)**: Kỹ thuật sản xuất, hỗ trợ nông thôn.
6.  **xAI-CN (Công nghiệp)**: Quản lý khu công nghiệp, sản xuất.
7.  **xAI-HC (Hành chính công)**: Hướng dẫn thủ tục, quy trình một cửa.
8.  **xAI-DN (DN & Đầu tư)**: Xúc tiến đầu tư và hỗ trợ doanh nghiệp địa phương.
9.  **xAI-GM (Giám sát)**: Tổng hợp báo cáo và giám sát hệ thống.

---

## 🚀 Hướng dẫn Cài đặt & Triển khai

### Yêu cầu Hệ thống
- Docker & Docker Compose
- Python 3.12+
- Node.js 20+ (cho phát triển Frontend)

### Triển khai nhanh với Docker

```bash
# 1. Clone repository
git clone https://github.com/your-username/xcb-platform.git
cd xcb-platform

# 2. Cấu hình môi trường
cp .env.example .env
# Chỉnh sửa .env với API Keys (LLM, Qdrant...)

# 3. Khởi chạy hệ thống
docker-compose up -d --build
```

- **Frontend**: [http://localhost:5173](http://localhost:5173)
- **Backend API**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Cơ sở dữ liệu (PostgreSQL)**: Port 5432
- **Vector DB (Qdrant)**: Port 6333

---

## 🛠 Kiến trúc Kỹ thuật

- **Backend**: FastAPI, SQLAlchemy, Alembic.
- **Frontend**: React (Vite), TailwindCSS, Framer Motion, Lucide Icons.
- **AI/LLM**: Tích hợp Qwen-2.5, GPT-4, Gemini (tùy cấu hình).
- **Database**: PostgreSQL (SQL), Qdrant (Vector).
- **Cache/Queue**: Redis.

---

## 📁 Cấu trúc Thư mục

```text
├── src/                    # Mã nguồn Backend
│   ├── agents/             # Định nghĩa 9 xAI agents
│   ├── database/           # Models & Migrations
│   ├── main.py             # FastAPI Entry point
│   └── api_router.py       # REST API Endpoints
├── web/                    # Mã nguồn Frontend (React)
├── alembic/                # Quản lý di cư database
├── docker-compose.yml      # Cấu hình Docker
└── README.md               # Tài liệu hướng dẫn
```

---

## 📧 Liên hệ & Hỗ trợ

**Đội ngũ Phát triển xCB**  
Email: support@xcb.local  
Website: [https://xcb.local](https://xcb.local)

© 2026 xCB - Nền tảng AI Công chức Việt Nam.
