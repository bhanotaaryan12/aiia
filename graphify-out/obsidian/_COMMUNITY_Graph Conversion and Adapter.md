---
type: community
members: 10
---

# Graph Conversion and Adapter

**Members:** 10 nodes

## Members
- [[dot-apply_confidence_decay()]] - code - backend/app/memory/privacy/isolation.py
- [[dot-build_graph()]] - code - backend/app/memory/graph/adapter.py
- [[dot-graph_to_extraction_dict()]] - code - backend/app/memory/graph/adapter.py
- [[dot-merge_duplicate_memories()]] - code - backend/app/memory/privacy/isolation.py
- [[Any_5]] - code
- [[Build NetworkX graph using Graphify's official build mechanism.]] - rationale - backend/app/memory/graph/adapter.py
- [[Decay confidence scores of old memories and mark low confidence ones as stale.]] - rationale - backend/app/memory/privacy/isolation.py
- [[Export a NetworkX graph into Graphify-compliant extraction dict format.]] - rationale - backend/app/memory/graph/adapter.py
- [[Graph_2]] - code
- [[Merge duplicate nodes into a primary node.]] - rationale - backend/app/memory/privacy/isolation.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Graph_Conversion_and_Adapter
SORT file.name ASC
```

## Connections to other communities
- 5 edges to [[_COMMUNITY_Memory Graph Demo Seeding]]
- 2 edges to [[_COMMUNITY_Tenant Graph Storage Backend]]
- 1 edge to [[_COMMUNITY_Context Builder and Ranking Engine]]
- 1 edge to [[_COMMUNITY_Graphify Memory Extraction Pipeline]]

## Top bridge nodes
- [[dot-build_graph()]] - degree 9, connects to 3 communities
- [[dot-graph_to_extraction_dict()]] - degree 6, connects to 1 community
- [[dot-apply_confidence_decay()]] - degree 5, connects to 1 community
- [[dot-merge_duplicate_memories()]] - degree 5, connects to 1 community