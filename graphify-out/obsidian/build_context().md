---
source_file: "backend/app/memory/context/builder.py"
type: "code"
community: "Context Builder and Ranking Engine"
location: "L13"
tags:
  - graphify/code
  - graphify/EXTRACTED
  - community/Context_Builder_and_Ranking_Engine
---

# build_context()

## Connections
- [[dot-before_agent_turn()]] - `calls` [EXTRACTED]
- [[dot-build_graph()]] - `calls` [EXTRACTED]
- [[dot-find_seed_nodes()]] - `calls` [EXTRACTED]
- [[dot-get_subgraph_nodes()]] - `calls` [EXTRACTED]
- [[dot-rank_nodes()]] - `calls` [EXTRACTED]
- [[Any]] - `references` [EXTRACTED]
- [[Build structured context package for a given user message. Returns dictionary…]] - `rationale_for` [EXTRACTED]
- [[ContextPackage]] - `calls` [EXTRACTED]
- [[EntityType]] - `uses` [INFERRED]
- [[GraphSearch]] - `uses` [INFERRED]
- [[GraphifyAdapter]] - `uses` [INFERRED]
- [[MemoryType]] - `uses` [INFERRED]
- [[MultiFactorRanker]] - `uses` [INFERRED]
- [[TenantGraphStorage]] - `calls` [EXTRACTED]
- [[api_build_context()]] - `calls` [EXTRACTED]
- [[builder.py]] - `contains` [EXTRACTED]
- [[lifecycle.py]] - `imports` [EXTRACTED]
- [[memory.py]] - `imports` [EXTRACTED]
- [[test_build_context_format()]] - `calls` [EXTRACTED]
- [[test_memory_system.py]] - `imports` [EXTRACTED]
- [[test_tenant_isolation()]] - `calls` [EXTRACTED]

#graphify/code #graphify/EXTRACTED #community/Context_Builder_and_Ranking_Engine