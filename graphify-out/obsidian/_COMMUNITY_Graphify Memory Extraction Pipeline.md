---
type: community
members: 34
---

# Graphify Memory Extraction Pipeline

**Members:** 34 nodes

## Members
- [[dot-__init__()]] - code - backend/app/memory/extraction/pipeline.py
- [[dot-_generate_canonical_id()]] - code - backend/app/memory/extraction/pipeline.py
- [[dot-extract_from_message()]] - code - backend/app/memory/extraction/pipeline.py
- [[dot-from_graphify_dict()]] - code - backend/app/memory/types/models.py
- [[dot-from_graphify_dict()_1]] - code - backend/app/memory/types/models.py
- [[dot-to_graphify_dict()]] - code - backend/app/memory/types/models.py
- [[dot-to_graphify_dict()_1]] - code - backend/app/memory/types/models.py
- [[Any_6]] - code
- [[ConfidenceLevel]] - code - backend/app/memory/types/enums.py
- [[Convert to dictionary matching Graphify edge schema exactly.]] - rationale - backend/app/memory/types/models.py
- [[Convert to dictionary matching Graphify node schema exactly.]] - rationale - backend/app/memory/types/models.py
- [[EntityType]] - code - backend/app/memory/types/enums.py
- [[Enum]] - code
- [[Extract entities, preferences, facts, and relationships from a message.]] - rationale - backend/app/memory/extraction/pipeline.py
- [[ExtractionResult]] - code - backend/app/memory/types/models.py
- [[Extracts entities, preferences, facts, events, and relationships from text or…]] - rationale - backend/app/memory/extraction/pipeline.py
- [[MemoryEdge]] - code - backend/app/memory/types/models.py
- [[MemoryExtractionPipeline]] - code - backend/app/memory/extraction/pipeline.py
- [[MemoryNode]] - code - backend/app/memory/types/models.py
- [[MemoryType]] - code - backend/app/memory/types/enums.py
- [[Provenance]] - code - backend/app/memory/types/models.py
- [[RelationType]] - code - backend/app/memory/types/enums.py
- [[Verify Graphify schema validation and NetworkX graph assembly.]] - rationale - backend/tests/test_memory_system.py
- [[Verify explicit facts vs inferred preferences in extraction pipeline.]] - rationale - backend/tests/test_memory_system.py
- [[adapter.py]] - code - backend/app/memory/graph/adapter.py
- [[enums.py]] - code - backend/app/memory/types/enums.py
- [[models.py]] - code - backend/app/memory/types/models.py
- [[pipeline.py]] - code - backend/app/memory/extraction/pipeline.py
- [[retrievalsearch.py]] - code - backend/app/memory/retrieval/search.py
- [[str]] - code
- [[test_extraction_pipeline_explicit_vs_inferred()]] - code - backend/tests/test_memory_system.py
- [[test_graphify_adapter_validation_and_build()]] - code - backend/tests/test_memory_system.py
- [[test_memory_system.py]] - code - backend/tests/test_memory_system.py
- [[utc_now_iso()]] - code - backend/app/memory/types/models.py

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Graphify_Memory_Extraction_Pipeline
SORT file.name ASC
```

## Connections to other communities
- 18 edges to [[_COMMUNITY_Memory Graph Demo Seeding]]
- 10 edges to [[_COMMUNITY_Tenant Graph Storage Backend]]
- 9 edges to [[_COMMUNITY_Context Builder and Ranking Engine]]
- 4 edges to [[_COMMUNITY_Analytics and CDISC Export]]
- 1 edge to [[_COMMUNITY_Graph Conversion and Adapter]]
- 1 edge to [[_COMMUNITY_Pytest Test Environment Fixtures]]

## Top bridge nodes
- [[test_memory_system.py]] - degree 20, connects to 4 communities
- [[MemoryNode]] - degree 18, connects to 4 communities
- [[EntityType]] - degree 18, connects to 3 communities
- [[MemoryExtractionPipeline]] - degree 18, connects to 2 communities
- [[MemoryType]] - degree 15, connects to 2 communities