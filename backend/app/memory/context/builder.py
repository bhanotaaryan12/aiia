import logging
from typing import Dict, Any, List, Optional

from app.memory.graph.storage import TenantGraphStorage
from app.memory.graph.adapter import GraphifyAdapter
from app.memory.retrieval.search import GraphSearch
from app.memory.ranking.ranker import MultiFactorRanker
from app.memory.types.enums import EntityType, MemoryType
from app.memory.types.models import ContextPackage

logger = logging.getLogger(__name__)

def build_context(
    user_id: str,
    message: str,
    storage: Optional[TenantGraphStorage] = None,
    max_nodes: int = 25
) -> Dict[str, Any]:
    """
    Build structured context package for a given user message.
    Returns dictionary matching core requirement 6:
    {
      "user": {},
      "relevant_facts": [],
      "preferences": [],
      "recent_events": [],
      "related_entities": [],
      "active_projects": [],
      "conversation_context": [],
      "confidence": {}
    }
    """
    if storage is None:
        storage = TenantGraphStorage()

    # Load graph data for user
    graph_dict = storage.load_graph_dict(user_id)
    if not graph_dict.get("nodes"):
        return ContextPackage(user={"id": user_id, "status": "new_user"}).model_dump()

    # Build NetworkX graph
    graph = GraphifyAdapter.build_graph([graph_dict])

    # Find seed nodes & traverse
    seeds = GraphSearch.find_seed_nodes(graph, message, user_id)
    subgraph_node_ids = GraphSearch.get_subgraph_nodes(graph, seeds, max_hops=2)

    # Rank nodes
    ranked = MultiFactorRanker.rank_nodes(graph, list(subgraph_node_ids), seeds, message)
    top_ranked = ranked[:max_nodes]

    user_info: Dict[str, Any] = {"id": user_id}
    relevant_facts: List[Dict[str, Any]] = []
    preferences: List[Dict[str, Any]] = []
    recent_events: List[Dict[str, Any]] = []
    related_entities: List[Dict[str, Any]] = []
    active_projects: List[Dict[str, Any]] = []
    conversation_context: List[Dict[str, Any]] = []
    confidence_map: Dict[str, float] = {}

    for node_attrs, score in top_ranked:
        label = node_attrs.get("label", node_attrs.get("id"))
        confidence_map[label] = round(score, 3)

        e_type = node_attrs.get("entity_type")
        m_type = node_attrs.get("memory_type")

        item = {
            "id": node_attrs.get("id"),
            "label": label,
            "entity_type": e_type,
            "memory_type": m_type,
            "confidence_score": node_attrs.get("confidence_score", 1.0),
            "confidence_level": node_attrs.get("confidence", "EXTRACTED"),
            "properties": node_attrs.get("properties", {}),
            "relevance_score": round(score, 3)
        }

        if e_type == EntityType.USER.value:
            user_info.update(node_attrs.get("properties", {}))
            user_info["label"] = label
        elif e_type == EntityType.PREFERENCE.value or m_type == MemoryType.USER_PREFERENCE.value:
            preferences.append(item)
        elif e_type == EntityType.FACT.value or m_type == MemoryType.EXPLICIT_FACT.value:
            relevant_facts.append(item)
        elif e_type in (EntityType.EVENT.value, EntityType.TASK.value):
            recent_events.append(item)
        elif e_type == EntityType.PROJECT.value:
            active_projects.append(item)
        elif e_type == EntityType.CONVERSATION.value or m_type == MemoryType.SHORT_TERM.value:
            conversation_context.append(item)
        else:
            related_entities.append(item)

    pkg = ContextPackage(
        user=user_info,
        relevant_facts=relevant_facts,
        preferences=preferences,
        recent_events=recent_events,
        related_entities=related_entities,
        active_projects=active_projects,
        conversation_context=conversation_context,
        confidence=confidence_map
    )

    return pkg.model_dump()
