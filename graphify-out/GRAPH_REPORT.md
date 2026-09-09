# Graph Report - aiia-ctms  (2026-09-08)

## Corpus Check
- 123 files · ~50,803 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 732 nodes · 1874 edges · 56 communities (29 shown, 18 thin omitted)
- Extraction: 87% EXTRACTED · 13% INFERRED · 0% AMBIGUOUS · INFERRED: 251 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Community Hubs (Navigation)
- Analytics and CDISC Export
- Audit Logs and Document Management
- Next.js Frontend UI Pages
- Backend Service Infrastructure and Docker
- User Authentication and Access Control
- Graphify Memory Extraction Pipeline
- FHIR R4 Interoperability Routes
- Tenant Graph Storage Backend
- eCRF Forms and Data Queries
- Pharmacovigilance and Safety Management
- Context Builder and Ranking Engine
- Ethics Committees and Approvals
- Regulatory Compliance and Tracking
- Clinical Trials and Study Arms
- Memory Graph Demo Seeding
- Frontend Package Metadata and Build Config
- TypeScript Configuration Settings
- Visit Schedules and Tracking
- Context Memory API Routes
- Frontend Production Dependencies
- Graph Conversion and Adapter
- Domain Schema Data Models
- Frontend Development Dependencies
- FHIR Pydantic Data Schemas
- JWT Security and Password Hashing
- Three-Tier Backend Architecture
- NPM Package Run Scripts
- Graphify Workflows and Rules
- SQLAlchemy Async Database Layer
- Next.js Root Layout Component
- Backend Generator - Core Models
- Backend Generator - Schemas and Routes
- Backend Generator - Main API App
- Backend Generator - Seed Data
- Frontend Generator Script
- Next.js Application Configuration
- Tailwind CSS Styling Configuration
- Context Memory Module Root
- Pytest Test Environment Fixtures
- Database Key Constraints and UUIDs
- Next.js TypeScript Declaration
- Analytics API Endpoints Specification
- Sites API Endpoints Specification
- Users API Endpoints Specification
- Visits API Endpoints Specification
- Database Soft Delete Design Pattern
- Environment Secrets Configuration

## God Nodes (most connected - your core abstractions)
1. `BaseModel` - 140 edges
2. `seed_data()` - 39 edges
3. `Participant` - 29 edges
4. `GraphifyAdapter` - 24 edges
5. `get_current_user()` - 23 edges
6. `react` - 23 edges
7. `build_context()` - 21 edges
8. `TenantGraphStorage` - 21 edges
9. `api` - 20 edges
10. `formatDate()` - 20 edges

## Surprising Connections (you probably didn't know these)
- `Docker Compose Frontend Service` --implements--> `Next.js Frontend`  [INFERRED]
  docker-compose.yml → README.md
- `Docker Compose Backend Service` --implements--> `FastAPI Backend`  [INFERRED]
  docker-compose.yml → README.md
- `FastAPI Backend` --implements--> `FastAPI Dependency`  [INFERRED]
  README.md → backend/requirements.txt
- `Docker Compose Postgres Service` --implements--> `PostgreSQL Database`  [INFERRED]
  docker-compose.yml → README.md
- `PostgreSQL Database Schema` --implements--> `PostgreSQL Database`  [INFERRED]
  docs/database.md → README.md

## Import Cycles
- None detected.

## Communities (56 total, 18 thin omitted)

### Community 0 - "Analytics and CDISC Export"
Cohesion: 0.11
Nodes (56): get_dashboard(), AsyncSession, get, export_cdisc(), list_mappings(), AsyncSession, get, post (+48 more)

### Community 1 - "Audit Logs and Document Management"
Cohesion: 0.05
Nodes (57): list_audit_logs(), AsyncSession, get, list_documents(), AsyncSession, get, post, upload_document() (+49 more)

### Community 2 - "Next.js Frontend UI Pages"
Cohesion: 0.09
Nodes (26): COLORS, AuditPage(), DashboardLayout(), COLORS, DashboardPage(), ParticipantDetail(), ParticipantsPage(), PharmacovigilancePage() (+18 more)

### Community 3 - "Backend Service Infrastructure and Docker"
Cohesion: 0.05
Nodes (43): FastAPI Dependency, Pydantic Schema Validation, Uvicorn ASGI Server, Docker Compose Backend Service, Docker Compose Frontend Service, Docker Compose Postgres Service, Audit Trail Endpoints, CDISC Export Endpoints (+35 more)

### Community 4 - "User Authentication and Access Control"
Cohesion: 0.14
Nodes (34): get_me(), login(), AsyncSession, get, post, refresh_token(), create_user(), get_user() (+26 more)

### Community 5 - "Graphify Memory Extraction Pipeline"
Cohesion: 0.19
Nodes (21): MemoryExtractionPipeline, Extracts entities, preferences, facts, events, and relationships from text or…, Extract entities, preferences, facts, and relationships from a message., ConfidenceLevel, EntityType, MemoryType, RelationType, ExtractionResult (+13 more)

### Community 6 - "FHIR R4 Interoperability Routes"
Cohesion: 0.15
Nodes (29): get_adverse_event(), get_observation(), get_patient(), get_research_study(), get_research_subject(), AsyncSession, get, count_participants() (+21 more)

### Community 7 - "Tenant Graph Storage Backend"
Cohesion: 0.10
Nodes (18): Any, Load tenant graph as extraction dict compliant with Graphify schema., Save tenant graph dict to file storage., Delete storage file for a given user., TenantGraphStorage, MemoryPrivacyManager, Handles multi-tenant isolation, privacy safety, provenance auditing, decay, and…, Enforce strict cross-tenant memory isolation. (+10 more)

### Community 8 - "eCRF Forms and Data Queries"
Cohesion: 0.17
Nodes (25): create_data_query(), create_form(), create_form_field(), create_submission(), get_form_fields(), list_data_queries(), list_forms(), list_submissions() (+17 more)

### Community 9 - "Pharmacovigilance and Safety Management"
Cohesion: 0.19
Nodes (21): create_ae(), create_sae(), list_aes(), list_saes(), list_safety_signals(), AsyncSession, get, post (+13 more)

### Community 10 - "Context Builder and Ranking Engine"
Cohesion: 0.12
Nodes (17): build_context(), Any, Build structured context package for a given user message. Returns dictionary…, MultiFactorRanker, Any, Graph, Ranks memory nodes using relevance, proximity, confidence, and recency., Exponential decay based on timestamp age. (+9 more)

### Community 11 - "Ethics Committees and Approvals"
Cohesion: 0.20
Nodes (19): create_approval(), create_committee(), create_submission(), list_approvals(), list_committees(), list_submissions(), AsyncSession, get (+11 more)

### Community 12 - "Regulatory Compliance and Tracking"
Cohesion: 0.22
Nodes (18): create_checklist_item(), create_record(), list_checklists(), list_records(), AsyncSession, get, post, put (+10 more)

### Community 13 - "Clinical Trials and Study Arms"
Cohesion: 0.22
Nodes (18): create_study_arm(), create_trial(), get_trial(), get_trial_arms(), list_trials(), AsyncSession, get, post (+10 more)

### Community 14 - "Memory Graph Demo Seeding"
Cohesion: 0.14
Nodes (12): Populate seed memory graphs for demo users., seed_demo_data(), GraphifyAdapter, Any, Adapter encapsulating Graphify SDK / NetworkX graph operations. Keeps all…, Validate extraction dict against Graphify's official schema., Raise ValueError if extraction dict violates Graphify schema., AgentMemoryLifecycle (+4 more)

### Community 15 - "Frontend Package Metadata and Build Config"
Cohesion: 0.11
Nodes (18): name, private, version, autoprefixer, axios, clsx, date-fns, @hookform/resolvers (+10 more)

### Community 16 - "TypeScript Configuration Settings"
Cohesion: 0.11
Nodes (17): compilerOptions, allowJs, esModuleInterop, incremental, isolatedModules, jsx, lib, module (+9 more)

### Community 17 - "Visit Schedules and Tracking"
Cohesion: 0.23
Nodes (15): create_participant_visit(), create_visit_definition(), list_participant_visits(), list_visit_definitions(), AsyncSession, get, post, put (+7 more)

### Community 18 - "Context Memory API Routes"
Cohesion: 0.24
Nodes (14): api_build_context(), api_decay(), api_delete_node(), api_forget(), api_get_nodes(), api_ingest_memory(), ContextRequest, ForgetRequest (+6 more)

### Community 19 - "Frontend Production Dependencies"
Cohesion: 0.15
Nodes (13): dependencies, axios, clsx, date-fns, @hookform/resolvers, lucide-react, next, react (+5 more)

### Community 20 - "Graph Conversion and Adapter"
Cohesion: 0.27
Nodes (6): Graph, Build NetworkX graph using Graphify's official build mechanism., Export a NetworkX graph into Graphify-compliant extraction dict format., Any, Merge duplicate nodes into a primary node., Decay confidence scores of old memories and mark low confidence ones as stale.

### Community 21 - "Domain Schema Data Models"
Cohesion: 0.22
Nodes (9): Audit Log & System Entities, Ethics Committee Entities, eCRF / EDC Entities, Participant Entities, Pharmacovigilance Entities, Regulatory Tracking Entities, Sites & Investigators Entities, Trial Management Entities (+1 more)

### Community 22 - "Frontend Development Dependencies"
Cohesion: 0.25
Nodes (8): devDependencies, autoprefixer, postcss, tailwindcss, @types/node, @types/react, @types/react-dom, typescript

### Community 23 - "FHIR Pydantic Data Schemas"
Cohesion: 0.52
Nodes (6): FHIRAdverseEvent, FHIRObservation, FHIRPatient, FHIRResearchStudy, FHIRResearchSubject, FHIRResource

### Community 24 - "JWT Security and Password Hashing"
Cohesion: 0.33
Nodes (6): Passlib Bcrypt Password Hashing, Python Jose JWT, Auth Endpoints, API Authentication, Bcrypt Password Hashing, JWT-Based Authentication

### Community 25 - "Three-Tier Backend Architecture"
Cohesion: 0.33
Nodes (6): API Layer (FastAPI Routes), Model Layer (SQLAlchemy ORM), Schema Layer (Pydantic Validation), Service Layer (Business Logic), Three-Tier Architecture Overview, Backend Permission Enforcement

### Community 26 - "NPM Package Run Scripts"
Cohesion: 0.40
Nodes (5): scripts, build, dev, lint, start

### Community 27 - "Graphify Workflows and Rules"
Cohesion: 0.50
Nodes (4): Graphify Knowledge Graph Rules, Graphify CLI Query, Graphify Subgraph Navigation, Graphify Pipeline Workflow

### Community 28 - "SQLAlchemy Async Database Layer"
Cohesion: 0.67
Nodes (4): Alembic Migration Tool, Asyncpg PostgreSQL Driver, SQLAlchemy Async Dependency, Async-First Architecture

## Knowledge Gaps
- **102 isolated node(s):** `Config`, `Config`, `Config`, `Config`, `Config` (+97 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 216 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **18 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `BaseModel` connect `Analytics and CDISC Export` to `Audit Logs and Document Management`, `User Authentication and Access Control`, `Graphify Memory Extraction Pipeline`, `FHIR R4 Interoperability Routes`, `Tenant Graph Storage Backend`, `eCRF Forms and Data Queries`, `Pharmacovigilance and Safety Management`, `Context Builder and Ranking Engine`, `Ethics Committees and Approvals`, `Regulatory Compliance and Tracking`, `Clinical Trials and Study Arms`, `Visit Schedules and Tracking`, `Context Memory API Routes`, `FHIR Pydantic Data Schemas`?**
  _High betweenness centrality (0.236) - this node is a cross-community bridge._
- **Why does `build_context()` connect `Context Builder and Ranking Engine` to `Graphify Memory Extraction Pipeline`, `Tenant Graph Storage Backend`, `Memory Graph Demo Seeding`, `Context Memory API Routes`, `Graph Conversion and Adapter`?**
  _High betweenness centrality (0.034) - this node is a cross-community bridge._
- **Why does `MemoryNode` connect `Graphify Memory Extraction Pipeline` to `Analytics and CDISC Export`, `Context Builder and Ranking Engine`, `Memory Graph Demo Seeding`, `Tenant Graph Storage Backend`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `seed_data()` (e.g. with `Base` and `timedelta`) actually correct?**
  _`seed_data()` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Are the 17 inferred relationships involving `Participant` (e.g. with `get_dashboard()` and `export_cdisc()`) actually correct?**
  _`Participant` has 17 INFERRED edges - model-reasoned connections that need verification._
- **Are the 10 inferred relationships involving `GraphifyAdapter` (e.g. with `build_context()` and `ConfidenceLevel`) actually correct?**
  _`GraphifyAdapter` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Are the 3 inferred relationships involving `get_current_user()` (e.g. with `Role` and `User`) actually correct?**
  _`get_current_user()` has 3 INFERRED edges - model-reasoned connections that need verification._