---
type: community
members: 20
---

# Memory Graph Demo Seeding

**Members:** 20 nodes

## Members
- [[dot-after_agent_turn()]] - code - backend/app/memory/middleware/lifecycle.py
- [[dot-assert_valid()]] - code - backend/app/memory/graph/adapter.py
- [[dot-before_agent_turn()]] - code - backend/app/memory/middleware/lifecycle.py
- [[dot-edges_to_models()]] - code - backend/app/memory/graph/adapter.py
- [[dot-nodes_to_models()]] - code - backend/app/memory/graph/adapter.py
- [[dot-validate_extraction()]] - code - backend/app/memory/graph/adapter.py
- [[Adapter encapsulating Graphify SDK  NetworkX graph operations. Keeps all…]] - rationale - backend/app/memory/graph/adapter.py
- [[AgentMemoryLifecycle]] - code - backend/app/memory/middleware/lifecycle.py
- [[Any_2]] - code
- [[Any_3]] - code
- [[GraphifyAdapter]] - code - backend/app/memory/graph/adapter.py
- [[Middleware  Hooks managing end-to-end conversation lifecycle Retrieve Memory…]] - rationale - backend/app/memory/middleware/lifecycle.py
- [[Populate seed memory graphs for demo users.]] - rationale - backend/app/memory/demo_seed.py
- [[Raise ValueError if extraction dict violates Graphify schema.]] - rationale - backend/app/memory/graph/adapter.py
- [[Step 1 & 2 Retrieve relevant graph memory & build structured context.]] - rationale - backend/app/memory/middleware/lifecycle.py
- [[Step 4, 5, 6 Extract new memories, validate + deduplicate, and persist to…]] - rationale - backend/app/memory/middleware/lifecycle.py
- [[Validate extraction dict against Graphify's official schema.]] - rationale - backend/app/memory/graph/adapter.py
- [[demo_seed.py]] - code - backend/app/memory/demo_seed.py
- [[lifecycle.py]] - code - backend/app/memory/middleware/lifecycle.py
- [[seed_demo_data()]] - code - backend/app/memory/demo_seed.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Memory_Graph_Demo_Seeding
SORT file.name ASC
```

## Connections to other communities
- 18 edges to [[_COMMUNITY_Graphify Memory Extraction Pipeline]]
- 9 edges to [[_COMMUNITY_Tenant Graph Storage Backend]]
- 5 edges to [[_COMMUNITY_Context Builder and Ranking Engine]]
- 5 edges to [[_COMMUNITY_Graph Conversion and Adapter]]
- 2 edges to [[_COMMUNITY_Context Memory API Routes]]

## Top bridge nodes
- [[GraphifyAdapter]] - degree 24, connects to 5 communities
- [[AgentMemoryLifecycle]] - degree 16, connects to 4 communities
- [[lifecycle.py]] - degree 5, connects to 3 communities
- [[dot-validate_extraction()]] - degree 5, connects to 2 communities
- [[Any_2]] - degree 6, connects to 1 community