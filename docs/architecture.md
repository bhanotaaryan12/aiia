# Architecture

## System Overview

The AIIA Clinical Trials Dashboard is a full-stack web application for managing Ayurveda clinical trials. It follows a clean three-tier architecture:

```
┌─────────────────────────────────┐
│        Presentation Layer       │
│   Next.js / React / TypeScript  │
│   Tailwind CSS / shadcn/ui      │
└──────────────┬──────────────────┘
               │ REST API (JSON)
               ▼
┌─────────────────────────────────┐
│        Application Layer        │
│   FastAPI / Python / Pydantic   │
│   JWT / RBAC / OpenAPI          │
├─────────────────────────────────┤
│   API Routes → Services →      │
│   Repositories → Database      │
└──────────────┬──────────────────┘
               │ SQLAlchemy ORM
               ▼
┌─────────────────────────────────┐
│        Data Layer               │
│   PostgreSQL / Audit Logs       │
│   Object Storage                │
└─────────────────────────────────┘
```

## Backend Architecture

### Layer Separation

1. **API Layer** (`app/api/`): HTTP request handling, input validation, response formatting
2. **Service Layer** (`app/services/`): Business logic, domain rules, workflow orchestration
3. **Model Layer** (`app/models/`): SQLAlchemy ORM models, database schema
4. **Schema Layer** (`app/schemas/`): Pydantic models for request/response validation

### Key Design Decisions

- **Async-first**: All database operations use async SQLAlchemy with asyncpg
- **UUID Primary Keys**: All entities use UUIDs for global uniqueness
- **Soft Deletes**: Critical entities use `is_deleted` flag instead of hard deletes
- **Audit Trail**: All mutations create append-only audit records
- **Pseudonymous IDs**: Participants are identified by system-generated pseudonymous IDs

### Domain Modules

```
Core CTMS          Clinical Data       Compliance & Safety
├── Trials         ├── eCRF/EDC       ├── Ethics/IEC
├── Protocols      ├── Validation     ├── Regulatory/CTRI
├── Sites          ├── Data Queries   ├── NDCT Rules
├── Investigators  ├── CDISC Export   ├── AE/SAE
├── Participants   └── FHIR R4       ├── Pharmacovigilance
├── Visits                            └── Audit Trail
└── Randomization
```

## Frontend Architecture

### Next.js App Router

- Server and client components
- Route-based code splitting
- API calls via axios with JWT interceptor

### Component Hierarchy

```
Layout (Sidebar + Topbar)
├── Dashboard (KPI Cards + Charts)
├── Trial Management
├── Site Management
├── Participant Management
├── Visit Schedule
├── Clinical Data (eCRF)
├── Ethics
├── Regulatory
├── Pharmacovigilance
├── Documents
├── Analytics
├── Audit Logs
└── Administration
```

## Security Architecture

```
Request → CORS → Rate Limit → JWT Verify → RBAC Check → Handler
                                                           │
                                                           ▼
                                                     Audit Log
```

### Role Hierarchy

```
SUPER_ADMIN (all permissions)
├── TRIAL_ADMIN (trial/site/user management)
├── PRINCIPAL_INVESTIGATOR (clinical operations)
├── STUDY_COORDINATOR (enrollment/visits/forms)
├── DATA_MANAGER (data quality/CDISC)
├── ETHICS_COMMITTEE (ethics workflow)
├── PHARMACOVIGILANCE_OFFICER (safety)
├── REGULATORY_OFFICER (regulatory tracking)
├── AUDITOR (read-only + audit)
└── VIEWER (read-only dashboards)
```

## Data Flow

### Clinical Trial Lifecycle

```
Trial Created → Ethics Submission → Ethics Approved
    → Regulatory Submission → CTRI Registered
    → Site Activation → Recruitment
    → Participant Screening → Consent → Enrollment
    → Randomization → Treatment Visits
    → eCRF Data Collection → Data Validation
    → AE/SAE Monitoring → Safety Reports
    → Study Completion → Data Lock → CDISC Export
```

## Interoperability

### CDISC

```
Internal Data → CDISC Mapping → SDTM Domains
                                ├── DM (Demographics)
                                ├── SV (Subject Visits)
                                ├── AE (Adverse Events)
                                └── (extensible)
```

### FHIR R4

```
Internal Models → FHIR Mapper → FHIR Resources
                                ├── Patient
                                ├── ResearchStudy
                                ├── ResearchSubject
                                ├── Observation
                                └── AdverseEvent
```

## Deployment Architecture

### Local Development
```
Docker Compose
├── PostgreSQL 16
├── FastAPI (uvicorn, hot reload)
└── Next.js (dev server)
```

### GCP Production
```
Cloud Load Balancer
├── Cloud Run (Frontend)
├── Cloud Run (Backend)
├── Cloud SQL (PostgreSQL)
├── Cloud Storage (Documents)
├── Secret Manager (Credentials)
├── Cloud Logging
├── Cloud Monitoring
├── Pub/Sub (Events)
└── Cloud Scheduler (Cron)
```
