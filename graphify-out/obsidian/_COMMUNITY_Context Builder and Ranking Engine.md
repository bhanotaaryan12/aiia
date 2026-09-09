---
type: community
members: 23
---

# Context Builder and Ranking Engine

**Members:** 23 nodes

## Members
- [[dot-calculate_recency_score()]] - code - backend/app/memory/ranking/ranker.py
- [[dot-find_seed_nodes()]] - code - backend/app/memory/retrieval/search.py
- [[dot-get_subgraph_nodes()]] - code - backend/app/memory/retrieval/search.py
- [[dot-rank_nodes()]] - code - backend/app/memory/ranking/ranker.py
- [[Any]] - code
- [[Any_1]] - code
- [[Build structured context package for a given user message. Returns dictionary…]] - rationale - backend/app/memory/context/builder.py
- [[ContextPackage]] - code - backend/app/memory/types/models.py
- [[Exponential decay based on timestamp age.]] - rationale - backend/app/memory/ranking/ranker.py
- [[Find seed nodes matching words in the query or user anchor.]] - rationale - backend/app/memory/retrieval/search.py
- [[Graph]] - code
- [[Graph_1]] - code
- [[GraphSearch]] - code - backend/app/memory/retrieval/search.py
- [[MultiFactorRanker]] - code - backend/app/memory/ranking/ranker.py
- [[Perform BFS traversal up to max_hops from seed nodes.]] - rationale - backend/app/memory/retrieval/search.py
- [[Rank nodes and return list of (node_dict, composite_score) sorted descending.]] - rationale - backend/app/memory/ranking/ranker.py
- [[Ranks memory nodes using relevance, proximity, confidence, and recency.]] - rationale - backend/app/memory/ranking/ranker.py
- [[Search and graph traversal methods on NetworkX graphs.]] - rationale - backend/app/memory/retrieval/search.py
- [[Verify build_context returns required 8-key structured context package.]] - rationale - backend/tests/test_memory_system.py
- [[build_context()]] - code - backend/app/memory/context/builder.py
- [[builder.py]] - code - backend/app/memory/context/builder.py
- [[ranker.py]] - code - backend/app/memory/ranking/ranker.py
- [[test_build_context_format()]] - code - backend/tests/test_memory_system.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Context_Builder_and_Ranking_Engine
SORT file.name ASC
```

## Connections to other communities
- 9 edges to [[_COMMUNITY_Graphify Memory Extraction Pipeline]]
- 5 edges to [[_COMMUNITY_Memory Graph Demo Seeding]]
- 4 edges to [[_COMMUNITY_Tenant Graph Storage Backend]]
- 2 edges to [[_COMMUNITY_Context Memory API Routes]]
- 1 edge to [[_COMMUNITY_Analytics and CDISC Export]]
- 1 edge to [[_COMMUNITY_Graph Conversion and Adapter]]

## Top bridge nodes
- [[build_context()]] - degree 21, connects to 5 communities
- [[builder.py]] - degree 8, connects to 3 communities
- [[test_build_context_format()]] - degree 5, connects to 3 communities
- [[ContextPackage]] - degree 4, connects to 2 communities
- [[GraphSearch]] - degree 6, connects to 1 community