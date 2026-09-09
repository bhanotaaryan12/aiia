# AIIA Clinical Trials Dashboard (CTMS)

> **A real-time, cloud-ready Clinical Trial Management System for Ayurveda research, with CDISC/FHIR interoperability, role-based KPIs, ethics and regulatory tracking, and integrated pharmacovigilance.**

Designed to support GCP-aligned clinical research workflows. This software supports compliance workflows but does not itself constitute legal or regulatory certification.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        USERS                                │
│   Admin │ PI │ Coordinator │ Data Manager │ Ethics │ PV     │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              NEXT.JS FRONTEND (React/TypeScript)            │
│              Tailwind CSS │ shadcn/ui │ Recharts            │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              FASTAPI BACKEND (Python)                       │
│   JWT/RBAC │ Pydantic │ SQLAlchemy │ OpenAPI               │
├─────────────┬─────────────┬─────────────────────────────────┤
│  CORE CTMS  │ CLINICAL    │ COMPLIANCE & SAFETY             │
│  Trials     │ eCRF/EDC    │ Ethics/IEC                      │
│  Sites      │ Validation  │ Regulatory/CTRI                 │
│  Participants│ CDISC      │ NDCT Rules 2019                 │
│  Visits     │ FHIR R4    │ AE/SAE/PV                       │
│  Randomize  │            │ Audit Trail                      │
└─────────────┴──────┬──────┴─────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              POSTGRESQL DATABASE                            │
│   40+ Tables │ UUID PKs │ Audit Logs │ Soft Deletes        │
└─────────────────────────────────────────────────────────────┘
```

---

## 📋 Prerequisites

- **Docker & Docker Compose** (recommended)
- OR:
  - Python 3.11+
  - Node.js 20+
  - PostgreSQL 16+

---

## 🚀 Quick Start (Docker)

```bash
# Clone and enter the project
cd aiia-ctms

# Copy environment config
cp .env.example .env

# Start all services
docker compose up --build

# The application will:
# 1. Start PostgreSQL
# 2. Run database migrations
# 3. Seed demo data
# 4. Start backend at http://localhost:8000
# 5. Start frontend at http://localhost:3000
```

---

## 🛠️ Manual Development Setup

### Database

```bash
# Create PostgreSQL database
createdb aiia_ctms

# Or with Docker
docker run -d --name aiia-db \
  -e POSTGRES_USER=aiia \
  -e POSTGRES_PASSWORD=aiia_dev_password \
  -e POSTGRES_DB=aiia_ctms \
  -p 5432:5432 \
  postgres:16-alpine
```

### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy env file
cp ../.env.example .env
# Edit .env with your database URL

# Run migrations
alembic upgrade head

# Seed demo data
python -m app.seed

# Start server
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

---

## 🔑 Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| **Super Admin** | admin@aiia.gov.in | Demo@12345 |
| **Trial Admin** | trialadmin@aiia.gov.in | Demo@12345 |
| **Principal Investigator** | pi@aiia.gov.in | Demo@12345 |
| **Study Coordinator** | coordinator@aiia.gov.in | Demo@12345 |
| **Data Manager** | datamanager@aiia.gov.in | Demo@12345 |
| **Ethics Committee** | ethics@aiia.gov.in | Demo@12345 |
| **PV Officer** | pv@aiia.gov.in | Demo@12345 |
| **Regulatory Officer** | regulatory@aiia.gov.in | Demo@12345 |
| **Auditor** | auditor@aiia.gov.in | Demo@12345 |
| **Viewer** | viewer@aiia.gov.in | Demo@12345 |

---

## 📦 Core Modules

### Trial Management
- Create and manage clinical trials with full lifecycle tracking
- Protocol management with versioning
- Study arms and interventions
- Trial milestones and timeline

### Site & Investigator Management
- Multi-site trial support
- Investigator assignment and tracking
- Site performance KPIs

### Participant Management
- Pseudonymous participant IDs
- Consent tracking
- Screening and enrollment workflow
- Randomization engine

### Visits & Scheduling
- Configurable visit definitions
- Automated scheduling
- Overdue visit detection
- Visit compliance tracking

### eCRF / EDC
- Configurable electronic case report forms
- Dynamic form rendering
- Real-time validation
- Data queries and quality scoring

### Ethics / IEC
- Ethics submission workflow
- Approval tracking with expiry alerts
- Protocol amendment management
- Renewal tracking

### Regulatory / CTRI
- CTRI registration tracking
- NDCT Rules 2019 compliance checklist
- Regulatory deadline management

### Pharmacovigilance
- Adverse Event (AE) reporting
- Serious Adverse Event (SAE) workflow
- Causality assessment
- Safety signal detection
- Safety dashboards

### CDISC Interoperability
- CDASH-inspired data collection
- SDTM-style export (CSV/JSON)
- Configurable domain mappings

### FHIR R4
- Patient, ResearchStudy, ResearchSubject, Observation, AdverseEvent resources
- RESTful FHIR endpoints

### 🧠 Context Memory Engine (Graphify-Powered)
- Multi-tenant isolated graph memory storage (`TenantGraphStorage`)
- Deterministic and semantic extraction pipeline (`MemoryExtractionPipeline`)
- Confidence tracking (`EXTRACTED` vs `INFERRED`) and provenance auditing
- Multi-factor memory ranking (`MultiFactorRanker`) combining relevance, proximity, confidence, and recency decay
- NetworkX / Graphify schema adapter (`GraphifyAdapter`)
- REST APIs under `/api/v1/memory` (`/context`, `/ingest`, `/nodes`, `/forget`, `/decay`)
- Persistent codebase knowledge graph in `graphify-out/` (interactive HTML, JSON, and Obsidian vault)

### 🎭 Presentation Walkthrough & Demo Safeguards
- Strictly restricted to designated demo account (`admin@aiia.gov.in`) via `/api/v1/demo/records`
- Built-in interactive study walkthrough panels:
  - **Protocol Review** (`/dashboard/study/protocol-review`)
  - **Operational Handoff** (`/dashboard/study/operational-handoff`)
  - **Data Safeguards** (`/dashboard/study/data-safeguards`)
  - **Clinical Site Monitoring & SDV** (`/dashboard/study/clinical-monitoring`)
  - **Pharmacovigilance & Safety Surveillance** (`/dashboard/study/safety-surveillance`)
  - **CDISC SDTM Standards & Regulatory Export** (`/dashboard/study/cdisc-standards`)
- Pre-seeded demo context memory graph and realistic trial milestone notifications

### Analytics & Dashboards
- Real-time KPIs from live database
- Role-specific dashboards
- Recruitment trends
- Site performance comparison
- Safety analytics

### Audit Trail
- Append-only audit log
- All critical actions tracked
- User, timestamp, action, entity, old/new values
- Searchable audit viewer

---

## 🔒 Security

- JWT authentication with access/refresh tokens
- Role-Based Access Control (RBAC) with 10 roles
- Granular permissions enforced on backend
- Pseudonymous participant IDs
- Password hashing with bcrypt
- CORS configuration
- Request validation with Pydantic
- Secure file upload validation
- Environment-based secrets
- MFA-ready architecture

---

## 📡 API Documentation

- **OpenAPI/Swagger**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

---

## 🧪 Testing

```bash
# Backend unit & memory system tests
cd backend
python -m pytest tests/test_memory_system.py -v

# Run full test suite with PYTHONPATH
PYTHONPATH=backend pytest tests/ -v

# Frontend TypeScript type check
cd frontend
npx tsc --noEmit
```

---

## 🗺️ Codebase Knowledge Graph (Graphify)

The codebase is indexed as a knowledge graph using [Graphify](https://github.com/safishamsi/graphify):

- **Interactive Visualizer**: Open `graphify-out/graph.html` in any browser.
- **Audit & Topology Report**: `graphify-out/GRAPH_REPORT.md` (732 nodes, 1,874 edges across 56 communities).
- **Obsidian Vault**: Markdown graph notes in `graphify-out/obsidian/`.
- **CLI Graph Queries**:
  ```bash
  # Query components and connections
  graphify query "context memory"
  
  # Deep-dive into specific abstractions
  graphify explain "build_context"
  graphify explain "TenantGraphStorage"
  ```

---

## ☁️ GCP Deployment Architecture

```
Internet → Cloud Load Balancer → Cloud Run (Frontend)
                                → Cloud Run (Backend)
                                → Cloud SQL (PostgreSQL)

Supporting services:
- Cloud Storage (documents)
- Secret Manager (credentials)
- Cloud Logging & Monitoring
- Pub/Sub (async events)
- Cloud Scheduler (cron jobs)
```

Local development does NOT require GCP credentials.

---

## 📁 Project Structure

```
aiia-ctms/
├── frontend/           # Next.js 14 + React + TypeScript
│   ├── app/           # App Router pages (Dashboard, Study Walkthrough, etc.)
│   ├── components/    # UI components (DemoRecordPanel, Charts, Forms)
│   ├── lib/           # Utilities, API client, auth
│   └── types/         # TypeScript types
├── backend/            # FastAPI + Python
│   ├── app/
│   │   ├── api/       # REST API routes (V1 endpoints, Memory, Demo)
│   │   ├── core/      # Config, security, database
│   │   ├── memory/    # Graphify Context Memory Engine
│   │   │   ├── context/     # Context builder
│   │   │   ├── extraction/  # Fact & preference extractor
│   │   │   ├── graph/       # Graphify adapter & tenant storage
│   │   │   ├── middleware/  # Agent conversation lifecycle
│   │   │   ├── privacy/     # Tenant isolation & forgetting
│   │   │   ├── ranking/     # Multi-factor node ranker
│   │   │   └── types/       # Enums, models & schemas
│   │   ├── models/    # SQLAlchemy models
│   │   ├── schemas/   # Pydantic schemas
│   │   ├── services/  # Business logic
│   │   └── seed.py    # Database & notification seeder
│   ├── tests/         # Unit & memory system test suite
│   ├── data/memory/   # Tenant-isolated JSON graph storage
│   └── alembic/       # Database migrations
├── graphify-out/       # Graphify outputs (graph.html, graph.json, GRAPH_REPORT.md)
├── docs/               # Architecture & database documentation
├── infra/              # Infrastructure configs
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## ⚠️ Known Limitations

1. **Authentication**: MFA is architecturally supported but not implemented in MVP
2. **Real-time**: Uses polling; WebSocket/SSE can be added
3. **CDISC**: SDTM export covers DM, SV, AE domains; extensible for more
4. **FHIR**: Core resources implemented; full FHIR server not included
5. **CTRI**: Tracking/workflow layer only — no direct CTRI API integration
6. **Email/SMS**: Console backend for development; provider abstraction ready
7. **File Storage**: Local storage for development; GCS abstraction ready
8. **Regulatory**: Configurable compliance workflows, not legal certification

---

## 📄 License

Proprietary - AIIA (All India Institute of Ayurveda)

---

## 🏥 Compliance Disclaimer

This platform is designed to support GCP-aligned clinical research workflows for Ayurveda studies. It provides configurable compliance tracking for regulatory requirements including NDCT Rules 2019, CTRI registration, and ethics committee workflows.

**This software does not constitute legal or regulatory certification.** Regulatory requirements are configurable and should be validated by qualified regulatory professionals. The system supports compliance workflows but organizations must ensure their own regulatory compliance.
