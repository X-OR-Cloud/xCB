<div align="center">

# 🤖 xHR — AI-native HR Platform

**Nền tảng quản lý nhân sự thông minh cho Thinh Long Group**

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://postgresql.org)
[![Claude AI](https://img.shields.io/badge/Claude-Anthropic-D97706?style=for-the-badge&logo=anthropic&logoColor=white)](https://anthropic.com)
[![Telegram](https://img.shields.io/badge/Telegram-Bot_API-26A5E4?style=for-the-badge&logo=telegram&logoColor=white)](https://core.telegram.org/bots)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://docker.com)

> **5 AI agents chuyên biệt** — tự động hoá quy trình HR xuất khẩu lao động, đào tạo và quản lý nội bộ thông qua Telegram Bot, được hỗ trợ bởi Claude AI của Anthropic.

</div>

---

## 📋 Mục lục

- [Tổng quan](#-tổng-quan)
- [Kiến trúc hệ thống](#-kiến-trúc-hệ-thống)
- [5 MOLTY Agents](#-5-molty-agents)
- [Tính năng](#-tính-năng)
- [Cài đặt & Chạy](#-cài-đặt--chạy)
- [Cấu hình](#-cấu-hình)
- [API Endpoints](#-api-endpoints)
- [Database Schema](#-database-schema)
- [Scheduler — Tác vụ tự động](#-scheduler--tác-vụ-tự-động)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)

---

## 🎯 Tổng quan

**xHR** là nền tảng HR AI-native được xây dựng riêng cho **Thinh Long Group** — công ty xuất khẩu lao động và đào tạo nghề tại Việt Nam. Thay vì giao diện web phức tạp, nhân viên tương tác với hệ thống **hoàn toàn qua Telegram**, nhận hỗ trợ tức thì từ các AI agent chuyên biệt theo từng phòng ban.

### Vấn đề giải quyết

| Trước xHR | Sau xHR |
|---|---|
| Tra cứu thủ công trên Excel | Truy vấn tức thì qua Telegram |
| Quên nhắc đóng BHXH | Tự động nhắc ngày 20 hàng tháng |
| Hộ chiếu hết hạn không hay | Cảnh báo tự động 90 ngày trước |
| Báo cáo mất hàng giờ | Dashboard tổng hợp trong 1 tin nhắn |
| Trình ký qua email chậm | Thông báo real-time qua Telegram |

---

## 🏗 Kiến trúc hệ thống

```
┌─────────────────────────────────────────────────────────────┐
│                        TELEGRAM USER                         │
└─────────────────────┬───────────────────────────────────────┘
                      │  HTTPS Webhook
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   FastAPI App (:8000)                        │
│   POST /webhook/telegram  ←  Telegram Bot API               │
│                      │                                       │
│              ┌───────▼────────┐                             │
│              │    ROUTER      │  lookup telegram_user_id     │
│              │  (src/router)  │  → NhanVien → phong_ban      │
│              └───────┬────────┘                             │
│       ┌──────┬───────┼───────┬──────┐                       │
│       ▼      ▼       ▼       ▼      ▼                       │
│   MOLTY  MOLTY   MOLTY   MOLTY  MOLTY                       │
│    -NB    -TV     -DT     -HC    -CEO                       │
│       └──────┴───────┼───────┴──────┘                       │
│                      │  Skills                               │
│              ┌───────▼────────┐                             │
│              │  Claude AI     │  intent classification        │
│              │  (Anthropic)   │  + business responses        │
│              └───────┬────────┘                             │
│                      │                                       │
│              ┌───────▼────────┐                             │
│              │  PostgreSQL    │  14 ORM models               │
│              └────────────────┘                             │
└─────────────────────────────────────────────────────────────┘
```

### Luồng xử lý tin nhắn

```
Telegram Update
    │
    ├─ 1. Verify webhook secret token
    ├─ 2. Deduplicate (update_id)
    ├─ 3. Lookup NhanVien by telegram_user_id
    ├─ 4. Dispatch to MOLTY agent (by phong_ban)
    │       ├─ A. Regex fast-path matching
    │       └─ B. Claude intent classification (fallback)
    ├─ 5. Execute skill (DB queries + Claude response)
    ├─ 6. Write AuditLog
    └─ 7. sendMessage via Telegram Bot API
```

---

## 🤖 5 MOLTY Agents

| Agent | Phòng ban | Chuyên môn | Skills |
|---|---|---|---|
| **MOLTY-NB** | `nhat_ban` | Thị trường Nhật Bản | Hồ sơ, Pipeline, Hộ chiếu/Visa, Báo cáo |
| **MOLTY-TV** | `thuy_en_vien`, `han_quoc` | Thuyền viên & Hàn Quốc | Đơn tàu, Hồ sơ TV, Thị trường HQ, Lịch khởi hành |
| **MOLTY-DT** | `dao_tao` | Trung tâm đào tạo | Điểm danh, Lịch học, Kết quả, Báo cáo đào tạo |
| **MOLTY-HC** | `hanh_chinh`, `ke_toan` | Hành chính & Kế toán | Trình ký, Nhân viên, Phí, BHXH, Hợp đồng |
| **MOLTY-CEO** | `lanh_dao`, `tgd` | Ban lãnh đạo | Dashboard, Rủi ro, Tài chính, Xuất khẩu |

### Ví dụ tương tác

```
👤 Nhân viên phòng Nhật Bản gửi:
   "Hộ chiếu nào sắp hết hạn?"

🤖 MOLTY-NB phản hồi:
   ⚠️ Hộ chiếu / Visa sắp hết hạn (≤ 90 ngày):

   • Nguyễn Văn A — hộ_chiếu | Hết hạn: 2025-05-10 (còn 57 ngày)
   • Trần Thị B — visa | Hết hạn: 2025-05-22 (còn 69 ngày)
```

```
👤 TGĐ gửi:
   "dashboard"

🤖 MOLTY-CEO phản hồi:
   📊 DASHBOARD TỔNG HỢP — THINH LONG GROUP
   📅 Ngày: 14/03/2026
   ───────────────────────────────────

   👷 Lao động xuất khẩu
     • Tổng hồ sơ: 342
     • Đã xuất cảnh: 218
     • Đang xử lý: 124

   👥 Nhân sự nội bộ: 28 nhân viên
   📋 Hợp đồng hiệu lực: 186
   💰 Phí chưa thu: 2,450,000,000 VND
   📝 Trình ký chờ duyệt: 3 văn bản
```

---

## ✨ Tính năng

### Core
- ✅ **Multi-agent routing** — tự động dispatch theo phòng ban
- ✅ **Dual-mode skill detection** — Regex (nhanh) + Claude AI (chính xác)
- ✅ **Message deduplication** — tránh xử lý trùng `update_id`
- ✅ **Typing indicator** — UX mượt mà trong khi xử lý
- ✅ **Audit log** — ghi lại toàn bộ hành động agent
- ✅ **Webhook secret verification** — bảo mật endpoint

### Tác vụ tự động (Scheduler)
- ✅ Nhắc điểm danh **4 buổi/ngày**
- ✅ **Cảnh báo hộ chiếu** hết hạn (ngưỡng 90 ngày, 7:00 AM)
- ✅ **Cảnh báo hợp đồng** hết hạn (ngưỡng 60 ngày, 7:30 AM)
- ✅ **Nhắc BHXH** ngày 20 hàng tháng (9:00 AM)
- ✅ **Báo cáo tuần** thứ Sáu 4:00 PM
- ✅ **Kiểm tra trình ký** mỗi 30 phút

---

## 🚀 Cài đặt & Chạy

### Yêu cầu
- Docker & Docker Compose
- Telegram Bot Token (từ [@BotFather](https://t.me/BotFather))
- Anthropic API Key
- Domain với HTTPS (để đăng ký Telegram webhook)

### 1. Clone & Cấu hình

```bash
git clone https://github.com/vulekaisar/xHR.git
cd xHR

# Copy và điền thông tin vào .env
cp .env.example .env
nano .env
```

### 2. Cấu hình `.env`

```env
DATABASE_URL=postgresql+asyncpg://xhr_user:xhr_password@db:5432/xhr_db
DATABASE_SYNC_URL=postgresql://xhr_user:xhr_password@db:5432/xhr_db
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_MODEL=claude-opus-4-6
TELEGRAM_BOT_TOKEN=123456789:ABCDefGHI...
TELEGRAM_WEBHOOK_SECRET=your-random-secret
APP_ENV=development
```

### 3. Khởi động

```bash
# Khởi động toàn bộ stack
docker-compose up --build

# Chạy migrations
docker-compose exec app alembic upgrade head

# Xem logs
docker-compose logs -f app
```

### 4. Đăng ký Telegram Webhook

```bash
# Thay YOUR_DOMAIN bằng domain thực của bạn (phải có HTTPS)
curl -X POST "http://localhost:8000/admin/register-webhook?webhook_url=https://YOUR_DOMAIN/webhook/telegram"
```

### 5. Phát triển local với ngrok

```bash
# Cài ngrok, sau đó:
ngrok http 8000

# Dùng URL ngrok để đăng ký webhook
curl -X POST "http://localhost:8000/admin/register-webhook?webhook_url=https://xxxx.ngrok.io/webhook/telegram"
```

---

## ⚙️ Cấu hình

| Biến môi trường | Mô tả | Bắt buộc |
|---|---|---|
| `DATABASE_URL` | Async PostgreSQL URL (asyncpg) | ✅ |
| `DATABASE_SYNC_URL` | Sync PostgreSQL URL (alembic) | ✅ |
| `ANTHROPIC_API_KEY` | Claude API key | ✅ |
| `CLAUDE_MODEL` | Model Claude (default: `claude-opus-4-6`) | ❌ |
| `TELEGRAM_BOT_TOKEN` | Token từ @BotFather | ✅ |
| `TELEGRAM_WEBHOOK_SECRET` | Secret token xác minh webhook | ✅ |
| `APP_ENV` | `development` \| `production` | ❌ |
| `PGADMIN_DEFAULT_EMAIL` | Email PgAdmin | ❌ |
| `PGADMIN_DEFAULT_PASSWORD` | Password PgAdmin | ❌ |

---

## 🔌 API Endpoints

| Method | Endpoint | Mô tả |
|---|---|---|
| `GET` | `/health` | Health check |
| `POST` | `/webhook/telegram` | Nhận Telegram Updates |
| `POST` | `/admin/register-webhook` | Đăng ký webhook với Telegram |
| `GET` | `/admin/status` | Trạng thái DB + config |
| `GET` | `/docs` | Swagger UI |

---

## 🗄 Database Schema

```
A — HR Profiles      : LaoDong, HoSoPhapLy
B — Training         : LopHoc, HocVienLop, DiemDanh
C — Export Pipeline  : PipelineTemplate, PipelineTienDo
D — Finance          : HopDong, PhiVaThanhToan
E — Internal HR      : NhanVien ★, TrinhKy
F — Seafarers        : ThuyEnVienDonHang
    Audit            : AuditLog
```

> ★ `NhanVien.telegram_user_id` — cột quan trọng nhất, dùng để map nhân viên với tài khoản Telegram.

### Migrations

```bash
# Tạo migration mới
docker-compose exec app alembic revision --autogenerate -m "ten_migration"

# Apply migrations
docker-compose exec app alembic upgrade head

# Rollback
docker-compose exec app alembic downgrade -1
```

---

## ⏰ Scheduler — Tác vụ tự động

| Job | Lịch | Gửi đến |
|---|---|---|
| Nhắc điểm danh (sáng sớm) | `06:15` hàng ngày | Phòng Đào tạo |
| Nhắc điểm danh (sáng) | `08:15` hàng ngày | Phòng Đào tạo |
| Nhắc điểm danh (chiều) | `13:15` hàng ngày | Phòng Đào tạo |
| Nhắc điểm danh (tối) | `19:45` hàng ngày | Phòng Đào tạo |
| Cảnh báo hộ chiếu/visa | `07:00` hàng ngày | Phòng NB + TV |
| Cảnh báo hợp đồng | `07:30` hàng ngày | Phòng HC |
| Kiểm tra trình ký | Mỗi `30 phút` | Người cần duyệt |
| Nhắc BHXH | Ngày `20` hàng tháng `09:00` | Phòng HC + KT |
| Báo cáo tuần | Thứ Sáu `16:00` | Ban Lãnh đạo |

*Tất cả theo timezone **Asia/Ho_Chi_Minh***

---

## 📁 Cấu trúc dự án

```
xHR/
├── 🐳 Dockerfile
├── 🐳 docker-compose.yml
├── 📦 requirements.txt
├── ⚙️  .env.example
├── 📖 CLAUDE.md                    ← Hướng dẫn cho AI coding assistant
├── alembic/                        ← Database migrations
│   ├── env.py
│   ├── script.py.mako
│   └── versions/
└── src/
    ├── main.py                     ← FastAPI app entry point
    ├── config.py                   ← Settings (pydantic-settings)
    ├── router.py                   ← Message router trung tâm
    ├── scheduler.py                ← APScheduler jobs
    ├── database/
    │   ├── models.py               ← 14 SQLAlchemy ORM models
    │   └── session.py              ← Async engine + session
    ├── integrations/
    │   ├── claude_client.py        ← Anthropic Claude wrapper
    │   └── telegram_bot.py         ← Telegram Bot API wrapper
    ├── agents/
    │   ├── base_agent.py           ← BaseAgent (abstract)
    │   ├── molty_nb.py             ← Agent Nhật Bản
    │   ├── molty_tv.py             ← Agent Thuyền viên/Hàn Quốc
    │   ├── molty_dt.py             ← Agent Đào tạo
    │   ├── molty_hc.py             ← Agent Hành chính/Kế toán
    │   └── molty_ceo.py            ← Agent Lãnh đạo/TGĐ
    └── skills/
        ├── nhat_ban/skills.py      ← 4 skills thị trường Nhật
        ├── thuy_en_vien/skills.py  ← 4 skills thuyền viên/Hàn Quốc
        ├── dao_tao/skills.py       ← 4 skills đào tạo
        ├── hanh_chinh/skills.py    ← 5 skills hành chính/kế toán
        └── lanh_dao/skills.py      ← 4 skills lãnh đạo
```

---

## 🔧 Services

| Service | URL | Mô tả |
|---|---|---|
| FastAPI App | `http://localhost:8000` | API chính |
| Swagger UI | `http://localhost:8000/docs` | API documentation |
| PgAdmin | `http://localhost:5050` | Quản lý database |
| PostgreSQL | `localhost:5432` | Database |

---

## 📜 License

Dự án nội bộ — **Thinh Long Group**. All rights reserved.

---

<div align="center">

**Built with ❤️ for Thinh Long Group**

*Powered by [Anthropic Claude](https://anthropic.com) · [FastAPI](https://fastapi.tiangolo.com) · [Telegram Bot API](https://core.telegram.org/bots)*

</div>
