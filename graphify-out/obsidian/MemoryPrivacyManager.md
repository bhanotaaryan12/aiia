---
source_file: "backend/app/memory/privacy/isolation.py"
type: "code"
community: "Tenant Graph Storage Backend"
location: "L12"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Tenant_Graph_Storage_Backend
---

# MemoryPrivacyManager

## Connections
- [[dot-__init__()_3]] - `method` [EXTRACTED]
- [[dot-apply_confidence_decay()]] - `method` [EXTRACTED]
- [[dot-forget_user_memories()]] - `method` [EXTRACTED]
- [[dot-merge_duplicate_memories()]] - `method` [EXTRACTED]
- [[dot-verify_tenant_access()]] - `method` [EXTRACTED]
- [[ForgetResponse]] - `uses` [INFERRED]
- [[GraphifyAdapter]] - `uses` [INFERRED]
- [[Handles multi-tenant isolation, privacy safety, provenance auditing, decay, and…]] - `rationale_for` [EXTRACTED]
- [[TenantGraphStorage]] - `uses` [INFERRED]
- [[isolation.py]] - `contains` [EXTRACTED]
- [[memory.py]] - `imports` [EXTRACTED]
- [[test_forgetting_api()]] - `calls` [EXTRACTED]
- [[test_memory_system.py]] - `imports` [EXTRACTED]
- [[test_tenant_isolation()]] - `calls` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/Tenant_Graph_Storage_Backend