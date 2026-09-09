---
type: community
members: 29
---

# Tenant Graph Storage Backend

**Members:** 29 nodes

## Members
- [[dot-__init__()_1]] - code - backend/app/memory/graph/storage.py
- [[dot-__init__()_2]] - code - backend/app/memory/middleware/lifecycle.py
- [[dot-__init__()_3]] - code - backend/app/memory/privacy/isolation.py
- [[dot-_get_user_file()]] - code - backend/app/memory/graph/storage.py
- [[dot-delete_tenant_graph()]] - code - backend/app/memory/graph/storage.py
- [[dot-forget_user_memories()]] - code - backend/app/memory/privacy/isolation.py
- [[dot-load_graph_dict()]] - code - backend/app/memory/graph/storage.py
- [[dot-save_graph_dict()]] - code - backend/app/memory/graph/storage.py
- [[dot-verify_tenant_access()]] - code - backend/app/memory/privacy/isolation.py
- [[Any_7]] - code
- [[AuditRecord]] - code - backend/app/memory/types/models.py
- [[Delete storage file for a given user.]] - rationale - backend/app/memory/graph/storage.py
- [[Enforce strict cross-tenant memory isolation.]] - rationale - backend/app/memory/privacy/isolation.py
- [[ForgetResponse]] - code - backend/app/memory/types/models.py
- [[Handles multi-tenant isolation, privacy safety, provenance auditing, decay, and…]] - rationale - backend/app/memory/privacy/isolation.py
- [[Load tenant graph as extraction dict compliant with Graphify schema.]] - rationale - backend/app/memory/graph/storage.py
- [[MemoryPrivacyManager]] - code - backend/app/memory/privacy/isolation.py
- [[Path]] - code
- [[Save tenant graph dict to file storage.]] - rationale - backend/app/memory/graph/storage.py
- [[TenantGraphStorage]] - code - backend/app/memory/graph/storage.py
- [[User-requested forgetting API.]] - rationale - backend/app/memory/privacy/isolation.py
- [[Verify context building, memory ingestion, and entity deduplication.]] - rationale - backend/tests/test_memory_system.py
- [[Verify strict multi-tenant isolation (User A cannot access or leak to User B).]] - rationale - backend/tests/test_memory_system.py
- [[Verify user-requested forgetting functionality.]] - rationale - backend/tests/test_memory_system.py
- [[isolation.py]] - code - backend/app/memory/privacy/isolation.py
- [[storage.py]] - code - backend/app/memory/graph/storage.py
- [[test_forgetting_api()]] - code - backend/tests/test_memory_system.py
- [[test_lifecycle_ingest_and_deduplication()]] - code - backend/tests/test_memory_system.py
- [[test_tenant_isolation()]] - code - backend/tests/test_memory_system.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Tenant_Graph_Storage_Backend
SORT file.name ASC
```

## Connections to other communities
- 10 edges to [[_COMMUNITY_Graphify Memory Extraction Pipeline]]
- 9 edges to [[_COMMUNITY_Memory Graph Demo Seeding]]
- 4 edges to [[_COMMUNITY_Context Builder and Ranking Engine]]
- 2 edges to [[_COMMUNITY_Analytics and CDISC Export]]
- 2 edges to [[_COMMUNITY_Context Memory API Routes]]
- 2 edges to [[_COMMUNITY_Graph Conversion and Adapter]]

## Top bridge nodes
- [[TenantGraphStorage]] - degree 21, connects to 4 communities
- [[MemoryPrivacyManager]] - degree 14, connects to 4 communities
- [[test_tenant_isolation()]] - degree 6, connects to 3 communities
- [[isolation.py]] - degree 6, connects to 2 communities
- [[ForgetResponse]] - degree 5, connects to 2 communities