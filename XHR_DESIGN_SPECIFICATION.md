# xHR AI-Native HR Platform - Design Specification

## 1. Project Overview
xHR is an AI-native HR Management platform designed for the **Thinh Long Group**. It leverages multi-agent AI systems to automate complex HR workflows, including international labor recruitment (Japan market), seafarer management, internal administration, and executive decision support.

The system is built on a **RAG (Retrieval-Augmented Generation)** architecture, allowing AI agents to "read" HR documents (PDFs, Images) and perform automated tasks like contract drafting, progress tracking, and internal approvals via Telegram.

---

## 2. Technology Stack

### Core Infrastructure
- **Backend**: Python 3.12, FastAPI (Async).
- **Frontend**: React 18, Vite, Tailwind CSS, Framer Motion (Glassmorphism UI).
- **Primary Database**: PostgreSQL 16 (Relational data).
- **Vector Database**: Qdrant (Knowledge base embeddings).
- **Caching & Queue**: Redis (Background workers, task tracking).
- **Object Storage**: S3-compatible storage (MinIO/CEPH) for document management.
- **Infrastructure**: Docker, Docker Compose.

### AI Engine
- **LLM Orchestration**: Hybrid model usage.
  - **Claude 3 Haiku**: Used for fast intent classification and simple extraction (Cost-optimized).
  - **Qwen-2.5-MAX**: Used for complex reasoning, RAG synthesis, and HR strategy.
- **OCR**: `pdf2image` + `Pillow` for document preprocessing.
- **Embeddings**: Local or API-based embeddings stored in Qdrant.

---

## 3. System Architecture

### Multi-Agent System (MOLTY Family)
1. **MOLTY-NB (Japan Market)**: Handles recruitment, Japanese training, and visa pipelines for the Japan market.
2. **MOLTY-TV (Seafarers)**: Manages foreign shipowner orders, vessel assignments, and seafarer certifications.
3. **MOLTY-HC (Admin & HR)**: Internal administrative tasks, office management, and employee records.
4. **MOLTY-CEO (Executive)**: Real-time system monitoring, high-level reporting, and risk assessment alerts.

### Interaction Channels
- **Web Dashboard**: High-end management interface for HR staff and Executives.
- **Telegram Bot**: Internal approval channel ("Trình ký"), employee self-service, and real-time alerts.

---

## 4. Database Schema (PostgreSQL)

### A — HR Profiles (`lao_dong`)
- Stores personal info, CMND, Passport, and market status (Japan, Korea, etc.).
- Related to `ho_so_phap_ly` (Documents) and `pipeline_tien_do`.

### B — Training (`lop_hoc`)
- Management of classes, subjects, teachers, and attendance (`diem_danh`).

### C — Export Pipeline (`pipeline_template`)
- Configurable steps for exporting labor (e.g., Step 1: Health check, Step 2: Training, Step 3: COE, Step 4: Visa).

### D — Finance & Contracts (`hop_dong`)
- Contract value, payment status, and fee breakdown (training fees, visa fees, etc.).

### E — Internal HR (`nhan_vien`)
- Employee record with `telegram_user_id` mapping for bot interactions.
- `Trình ký` (Approvals) table for digital workflows.

### F — Seafarers (`thuy_en_vien_don_hang`)
- Orders from shipowners, salary info in USD, and vessel types.

---

## 5. Knowledge Base (RAG)
- **TaiLieu table**: Tracks file ingestion status (OCR Progress, Vector Progress).
- **Processing Pipeline**:
  1. Upload PDF/Image to S3.
  2. OCR processing (extract text from scans).
  3. Chunking & Embedding.
  4. Upserting to Qdrant with metadata (Market, Department).

---

## 6. Frontend Blueprint

### Design Language: Glassmorphism
- **Colors**: Deep Slate (#0F172A), Electric Blue, Vibrant Purple.
- **Visuals**: Frosted glass effects, subtle gradients, micro-animations (Framer Motion).
- **Layout**: Sidebar navigation, Top search bar, Grid-based Dashboard widgets.

### Core Components
- **DashboardCEO**: Interactive Map, Strategic Alerts, Revenue Trend Charts (Mockdata integration).
- **DataManager**: Drag & Drop upload, real-time processing queue tracking.
- **AgentChat**: Side panel for interacting with specific MOLTY agents.

---

## 7. API Design Strategy
- **Restful API**: `/api/v1/...`
- **Async Endpoints**: Essential for OCR and AI generation.
- **Security**: JWT-based Auth (mapped with internal staff records).

---

## 8. Deployment & Scaling
- **Dockerized Environment**:
  - `xhr-app`: FastAPI backend.
  - `xhr-web`: Vite-based frontend.
  - `xhr-worker`: Background worker for OCR/Vectorizing.
- **Volumes**: Persistent storage for Postgres, Redis, and Qdrant data.
- **Environment Management**: `.env` file for API keys (Anthropic, Qwen, Redis URL).

---

## 9. Implementation Checklist for AI Rebuild
1. **Initialize DB**: Run Alembic migrations to build the schema.
2. **Setup RAG**: Configure Qdrant collection and embedding pipeline.
3. **Internal Auth**: Map Telegram User IDs to `nhan_vien` table.
4. **Agent Logic**: Implement `BaseAgent` class with tool-calling capabilities.
5. **UI Assembly**: Build React components using the Glassmorphism design tokens.
