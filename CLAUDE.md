# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

xHR is an AI-native HR platform for **Thinh Long Group** — a Vietnamese labor export and training company. It exposes 5 specialized Claude-powered agents via **Telegram Bot** (messaging platform), automating HR workflows across departments.

## Development Commands

```bash
# Start the full stack (app + PostgreSQL + PgAdmin)
docker-compose up

# Start in background
docker-compose up -d

# Rebuild after dependency changes
docker-compose up --build

# Run database migrations
docker-compose exec app alembic upgrade head

# View logs
docker-compose logs -f app
```

Services:
- FastAPI app: `http://localhost:8000`
- Health check: `GET /health`
- PgAdmin: `http://localhost:5050`
- PostgreSQL: port 5432

## Architecture

### Multi-Agent System

Incoming Telegram messages hit `/webhook/telegram` → **router** looks up the sender's department in `NhanVien` table (matched via `telegram_user_id`) → dispatches to the appropriate MOLTY agent:

| Department (`phong_ban`) | Agent | Role |
|---|---|---|
| `nhat_ban` | MOLTY-NB | Japan market operations |
| `thuy_en_vien`, `han_quoc` | MOLTY-TV | Seafarers / crew management |
| `dao_tao` | MOLTY-DT | Training center |
| `hanh_chinh`, `ke_toan` | MOLTY-HC | HR & admin |
| `lanh_dao`, `tgd` | MOLTY-CEO | Executive dashboard |

### Telegram Webhook Flow

1. Telegram sends `POST /webhook/telegram` with an `Update` object (HTTPS only, verified by Telegram token).
2. The router extracts `message.from.id` (`telegram_user_id`) and the message text.
3. Department lookup runs against the `NhanVien` table.
4. The matching MOLTY agent processes the message and replies via the **Telegram Bot API** (`sendMessage`).

### Skill Routing (inside each agent)

Each agent (`src/agents/`) extends `BaseAgent` and routes to skills via:
1. **Regex pattern matching** (fast path — defined per-agent)
2. **Claude intent classification** (fallback for ambiguous messages)

Skills live in `src/skills/<department>/skills.py` and contain the actual business logic (DB queries, Claude calls, Telegram replies).

### Database (6 modules, all in `src/database/models.py`)

- **A - HR Profiles**: `LaoDong` (worker records), `HoSoPhapLy` (legal docs)
- **B - Training**: `LopHoc` (classes), `HocVienLop` (enrollment), `DiemDanh` (attendance)
- **C - Export Pipeline**: `PipelineTemplate`, `PipelineTienDo` (per-worker progress)
- **D - Finance**: `HopDong` (contracts), `PhiVaThanhToan` (fees/payments)
- **E - Internal HR**: `NhanVien` (employees), `TrinhKy` (approval workflow) — includes `telegram_user_id` column for identity mapping
- **F - Seafarers**: `ThuyEnVienDonHang` (ship orders)
- **Audit**: `AuditLog` — every agent action is logged here

### Key Integrations

- **`src/integrations/claude_client.py`**: Async Claude wrapper — temperature 0.2, supports single/multi-turn. Default model: `claude-opus-4-6`.
- **`src/integrations/telegram_bot.py`**: Telegram Bot API wrapper — webhook verification via secret token header (`X-Telegram-Bot-Api-Secret-Token`), async message sending via `httpx` to `https://api.telegram.org/bot<TOKEN>/sendMessage`.

### Scheduler (`src/scheduler.py`)

APScheduler runs automatic tasks on Vietnam timezone (`Asia/Ho_Chi_Minh`):
- Attendance checks at 6:15 AM, 8:15 AM, 1:15 PM, 7:45 PM
- Weekly report every Friday 4 PM
- Monthly BHXH reminder on 20th at 9 AM
- Passport expiry alerts daily 7 AM (90-day threshold)
- Contract expiry alerts daily 7:30 AM (60-day threshold)
- Signature workflow deadline checks every 30 min

Scheduled messages are pushed via the **Telegram Bot API** to the relevant user's `telegram_user_id`.

## Configuration

Copy `.env.example` to `.env`. Key variables:

```
DATABASE_URL          # asyncpg+postgresql://...
DATABASE_SYNC_URL     # postgresql://... (for alembic)
ANTHROPIC_API_KEY     # Claude API key
CLAUDE_MODEL          # default: claude-opus-4-6
TELEGRAM_BOT_TOKEN    # Telegram Bot token from @BotFather
TELEGRAM_WEBHOOK_SECRET  # Secret token for webhook verification
APP_ENV               # development | production
```

## Code Conventions

- **Async-first**: all I/O uses `async/await` (FastAPI, SQLAlchemy async sessions, httpx)
- **Vietnamese content**: all prompts, messages, and field names are in Vietnamese — maintain this
- **Structured logging**: use `structlog` for all log output, not `print`
- **Audit everything**: agent actions must be written to `AuditLog`
- **Message deduplication**: done via `update_id` (Telegram) before processing
- **Timezone**: always use `Asia/Ho_Chi_Minh` for datetimes
