# xCB Platform - Nền tảng Đa tác nhân AI phục vụ Công chức Địa phương

**xCB (x-OR Cloud Bureaucracy)** là giải pháp AI tiên tiến được thiết kế riêng cho cán bộ công chức cấp Tỉnh, Huyện, Xã tại Việt Nam. Hệ thống kết hợp sức mạnh của các tác nhân AI (AI Agents) chuyên biệt cùng khả năng lưu trữ và xử lý tri thức nghiệp vụ khổng lồ, giúp tối ưu hóa hiệu suất hành chính và hỗ trợ ra quyết định chính xác.

---

## 🚀 Tính năng Cốt lõi

### 1. Hệ thống Đa tác nhân xAI-CB (Multi-Agent System)
Hệ thống tích hợp 9 AI Agents chuyên trách cho từng lĩnh vực nghiệp vụ:
- **xAI-PL**: Tư vấn Pháp lý, giải đáp các nghị định, thông tư mới nhất.
- **xAI-GD**: Hỗ trợ nghiệp vụ Giáo dục và Đào tạo.
- **xAI-BH**: Chuyên gia Bảo hiểm xã hội và chính sách an sinh.
- **xAI-TN**: Quản lý tài nguyên, môi trường và đất đai.
- **xAI-NN**: Hỗ trợ kỹ thuật và chính sách nông nghiệp, nông thôn.
- **xAI-CN**: Tư vấn phát triển công nghiệp và hạ tầng.
- **xAI-HC**: Điều phối thủ tục hành chính công và dịch vụ một cửa.
- **xAI-DN**: Trợ lý hỗ trợ doanh nghiệp và thu hút đầu tư.
- **xAI-GM**: Hệ thống giám sát, tổng hợp và phân tích dữ liệu đa kênh.

### 2. Trung tâm Điều hành Dashboard Thông minh
- **Biểu đồ Hiệu suất AI**: Theo dõi số lượng nhiệm vụ AI hỗ trợ công chức theo Ngày/Tháng/Năm.
- **So sánh Trực quan**: Đường biểu đồ "Tổng nhiệm vụ" vs "AI xử lý" giúp đánh giá tỉ lệ tự động hóa.
- **Phân tích Lĩnh vực**: Biểu đồ đường (Line Chart) theo dõi biến động hồ sơ giữa các phòng ban.
- **KPI Real-time**: Theo dõi tỉ lệ đúng hạn, hồ sơ đang chờ và hồ sơ quá hạn ngay lập tức.

### 3. Kho Tri thức RAG (Retrieval Augmented Generation)
- **Quản lý Vector**: Chuyển đổi hàng triệu tài liệu pháp lý thành vector embeddings để tìm kiếm ngữ nghĩa.
- **Thống kê Phân bổ**: Theo dõi số lượng tài liệu tri thức trong từng lĩnh vực (Hành chính, Pháp luật, Đất đai...).
- **Semantic Search**: Tìm kiếm nội dung dựa trên ý nghĩa, giúp cán bộ tìm thấy căn cứ pháp lý chỉ trong vài giây.

### 4. Trung tâm Nạp dữ liệu xCB
- **Xử lý Thông minh**: Tích hợp OCR (nhận dạng ký tự quang học) và tự động hóa quy trình Vector hóa.
- **Hàng đợi Xử lý**: Theo dõi tiến độ nạp tri thức từ các tệp PDF, Word, Ảnh qua mockdata trực quan.
- **Quản lý Lưu trữ**: Giám sát dung lượng lưu trữ cấp độ Terabyte (TB) và dự báo tình hình sử dụng.

---

## 🛠 Công nghệ Sử dụng

- **Backend**: FastAPI (Python), SQLAlchemy, PostgreSQL.
- **AI/ML**: LangChain, OpenAI/Gemini SDK, Qdrant (Vector Database).
- **Frontend**: React.js, TailwindCSS, Framer Motion, Lucide React.
- **Infrastructure**: Docker, Docker Compose, Redis.

---

## 📦 Hướng dẫn Triển khai (Docker)

### 1. Yêu cầu Hệ thống
- Docker & Docker Compose (V2)
- Tối thiểu 4GB RAM

### 2. Khởi động nhanh
```bash
# Clone dự án
git clone [URL_GIAO_DIEN_GIT]
cd xCB

# Cấu hình môi trường
cp .env.example .env

# Khởi chạy toàn bộ hệ thống
docker-compose up -d --build
```

### 3. Truy cập Ứng dụng
- **Giao diện người dùng**: `http://localhost:5173`
- **Tài liệu API (Swagger)**: `http://localhost:8000/docs`

---

## 🤝 Liên hệ & Đóng góp
Dự án được phát triển bởi đội ngũ công nghệ vì sự nghiệp hiện đại hóa nền hành chính công Việt Nam.
- **Đơn vị**: x-OR Cloud
- **Phiên bản**: 2.0.0 (xCB Edition)
