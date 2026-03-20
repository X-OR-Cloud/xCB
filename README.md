# xCB Platform - Trợ lý AI Đa năng cho Cán bộ Công chức Địa phương

**xCB (x-OR Cloud Bureaucracy)** là nền tảng AI đột phá, được thiết kế để trở thành "người cộng sự số" đắc lực cho cán bộ công chức tại các cấp Tỉnh, Huyện, Xã. Hệ thống tích hợp các tác nhân AI (AI Agents) chuyên sâu không chỉ để hỗ trợ nghiệp vụ, tra cứu pháp luật mà còn trực tiếp **thực thi các quy trình tự động hóa** thay thế cho các tác vụ thủ công lặp lại.

---

## 🤖 Hệ thống AI Agents & Chức năng Cốt lõi

Hệ thống bao gồm 9 "Chuyên gia số" luôn sẵn sàng hỗ trợ 24/7:

1.  **xAI-PL (Trợ lý Pháp lý)**: Tra cứu nhanh các Nghị định, Thông tư; Giải thích quy định pháp luật; Kiểm tra hiệu lực văn bản pháp quy.
2.  **xAI-HC (Trợ lý Hành chính)**: Hỗ trợ nghiệp vụ một cửa; Hướng dẫn quy trình xử lý hồ sơ; Soạn thảo văn bản theo mẫu chuẩn.
3.  **xAI-GM (Trợ lý Giám sát)**: Cảnh báo hồ sơ quá hạn; Phân tích biến động dữ liệu kinh tế - xã hội; Tổng hợp báo cáo định kỳ tự động.
4.  **xAI-TN (Trợ lý Tài nguyên & Đất đai)**: Hỗ trợ tra cứu quy hoạch, chính sách bồi thường và quản lý môi trường.
5.  **xAI-NN (Trợ lý Nông nghiệp)**: Tư vấn chính sách hỗ trợ nông thôn mới, kỹ thuật canh tác và phòng chống dịch bệnh.
6.  **xAI-DN (Trợ lý Doanh nghiệp)**: Hỗ trợ thủ tục đầu tư, đăng ký kinh doanh và giải đáp chính sách cho doanh nghiệp.
7.  **xAI-GD (Trợ lý Giáo dục)**: Hỗ trợ nghiệp vụ sư phạm, quy định về tuyển sinh và quản lý bằng cấp.
8.  **xAI-BH (Trợ lý Bảo hiểm)**: Giải đáp các chính sách bảo hiểm xã hội, bảo hiểm y tế và an sinh xã hội.
9.  **xAI-CN (Trợ lý Công nghiệp)**: Tư vấn quy chuẩn khu công nghiệp, hạ tầng kỹ thuật và phát triển tiểu thủ công nghiệp.

---

## 🚀 Khả năng Thực thi & Tự động hóa Nghiệp vụ (Beyond Chat)

xCB không chỉ là một công cụ chat thông thường, mà là một **"Nhân viên số" (Digital Worker)** có khả năng thực hiện các nghiệp vụ thay cho con người:

### ⏱️ Tự động Rà soát & Cảnh báo Chủ động
AI không đợi cán bộ hỏi mà chủ động quét cơ sở dữ liệu định kỳ để:
*   Phát hiện và gửi thông báo nhắc lịch đóng **BHXH, Thuế** trước hạn.
*   Cảnh báo các **Hợp đồng, Giấy phép** sắp hết hạn trong 30-60 ngày tới.
*   Truy vết các khoản **Phí và Thanh toán** quá hạn để cán bộ kịp thời xử lý.

### 📝 Điều phối Luồng Trình ký & Phê duyệt
Tích hợp trực tiếp vào quy trình phê duyệt văn bản:
*   Tổng hợp danh sách văn bản đang chờ phê duyệt và gửi tóm tắt qua Telegram cho lãnh đạo.
*   Lãnh đạo có thể thực hiện thao tác duyệt/yêu cầu sửa đổi ngay trên giao diện chat.
*   Tự động cập nhật trạng thái vào hệ thống quản lý tập trung.

### 📂 Tự động hóa Nhập liệu & Xử lý Văn bản (OCR)
Giải phóng cán bộ khỏi các tác vụ nhập liệu thủ công:
*   **Trích xuất dữ liệu**: Cán bộ chỉ cần gửi ảnh chụp CCCD, Sổ đỏ hoặc văn bản qua chat, AI tự động dùng OCR để bóc tách thông tin và điền vào các bảng biểu liên quan.
*   **Phân loại tri thức tự động**: Các văn bản pháp quy mới nạp vào sẽ được AI tự động phân loại, gắn nhãn và vector hóa vào kho tri thức RAG.

### 📊 Tự động Tổng hợp Báo cáo Số liệu
*   Tự động truy xuất dữ liệu từ nhiều nguồn (PostgreSQL, Vector DB, Excel) để xây dựng báo cáo phân tích theo yêu cầu bằng ngôn ngữ tự nhiên, không cần lập trình viên can thiệp.

---

## 💡 Kịch bản Tương tác tiêu biểu

### 1. Xử lý hồ sơ thông minh
*   **Cán bộ**: (Gửi ảnh chụp Nghị định mới) "Nạp văn bản này vào kho tri thức và tóm tắt các điểm quan trọng cho tôi."
*   **AI Agent**: "Đã nhận diện file Scan. Tôi đã phân loại vào mục 'Pháp luật Đất đai' và tóm tắt 03 điểm mới về giá đền bù tại Điều 20... (Hiển thị tóm tắt)."

### 2. Thực thi nghiệp vụ tự động
*   **AI (Chủ động gửi tin nhắn)**: "Chào anh/chị, tôi phát hiện có 05 hợp đồng thuê đất tại xã X sẽ hết hạn vào tháng tới. Tôi đã chuẩn bị sẵn danh sách và mẫu thông báo gia hạn, anh/chị có muốn gửi duyệt ngay không?"
*   **Cán bộ**: "Duyệt gửi cho lãnh đạo danh sách này."

---

## 🛠 Công cụ & Phương thức Tương tác

### 📱 Telegram Bot Integration
*   Phản hồi tức thì, giao diện chat thân thiện.
*   Hỗ trợ tương tác command-base cho các lệnh thực thi nhanh.

### 🌐 Smart Dashboard (Web Interface)
*   Trung tâm điều hành tập trung để giám sát các Robot đang chạy tự động.
*   Quản lý trực quan luồng dữ liệu và kho tri thức.

---

## 🚀 Hướng dẫn Triển khai Nhanh

1.  **Cấu hình**: Cập nhật file `.env` với API Key (Claude/Gemini) và Telegram Token.
2.  **Khởi tạo**: Chạy `docker-compose up -d`.
3.  **Tác vụ tự động**: Thiết lập các cron-job trong hệ thống để AI chủ động rà soát dữ liệu.

---
*Dự án được phát triển bởi đội ngũ công nghệ vì sự nghiệp hiện đại hóa nền hành chính công Việt Nam.*
