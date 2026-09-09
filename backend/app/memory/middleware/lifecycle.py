import logging
from typing import Dict, Any, Optional, Tuple

from app.memory.context.builder import build_context
from app.memory.extraction.pipeline import MemoryExtractionPipeline
from app.memory.graph.storage import TenantGraphStorage
from app.memory.graph.adapter import GraphifyAdapter

logger = logging.getLogger(__name__)

class AgentMemoryLifecycle:
    """
    Middleware / Hooks managing end-to-end conversation lifecycle:
    Retrieve Memory -> Build Context -> LLM / Agent -> Extract Memories -> Deduplicate -> Persist to Graphify
    """

    def __init__(self, storage: Optional[TenantGraphStorage] = None):
        self.storage = storage or TenantGraphStorage()
        self.extractor = MemoryExtractionPipeline()

    def before_agent_turn(
        self, user_id: str, message: str, session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Step 1 & 2: Retrieve relevant graph memory & build structured context.
        """
        logger.info(f"Retrieving memory & building context for user {user_id}...")
        context_package = build_context(user_id=user_id, message=message, storage=self.storage)
        return context_package

    def after_agent_turn(
        self,
        user_id: str,
        message: str,
        response_text: str,
        session_id: Optional[str] = None,
        source_message_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Step 4, 5, 6: Extract new memories, validate + deduplicate, and persist to Graphify store.
        """
        logger.info(f"Extracting & persisting memories for user {user_id}...")
        
        # 1. Extract from user turn
        user_ext = self.extractor.extract_from_message(
            user_id=user_id,
            message=message,
            role="user",
            session_id=session_id,
            source_message_id=source_message_id
        )

        # 2. Extract from assistant turn if available
        asst_ext = None
        if response_text:
            asst_ext = self.extractor.extract_from_message(
                user_id=user_id,
                message=response_text,
                role="assistant",
                session_id=session_id,
                source_message_id=source_message_id
            )

        # Combine nodes & edges
        new_nodes_dict = [n.to_graphify_dict() for n in user_ext.nodes]
        new_edges_dict = [e.to_graphify_dict() for e in user_ext.edges]

        if asst_ext:
            new_nodes_dict.extend([n.to_graphify_dict() for n in asst_ext.nodes])
            new_edges_dict.extend([e.to_graphify_dict() for e in asst_ext.edges])

        # Load existing graph
        existing_graph_dict = self.storage.load_graph_dict(user_id)
        existing_nodes = {n["id"]: n for n in existing_graph_dict.get("nodes", [])}
        existing_edges = {(e["source"], e["target"], e.get("relation")): e for e in existing_graph_dict.get("edges", [])}

        # Deduplicate & merge nodes
        for node_d in new_nodes_dict:
            nid = node_d["id"]
            if nid in existing_nodes:
                # Update existing node metadata instead of duplicating
                existing_nodes[nid]["updated_at"] = node_d["updated_at"]
                if "properties" in node_d:
                    existing_nodes[nid].setdefault("properties", {}).update(node_d["properties"])
            else:
                existing_nodes[nid] = node_d

        # Deduplicate & merge edges
        for edge_d in new_edges_dict:
            key = (edge_d["source"], edge_d["target"], edge_d.get("relation"))
            if key in existing_edges:
                existing_edges[key]["updated_at"] = edge_d["updated_at"]
                existing_edges[key]["weight"] = min(5.0, float(existing_edges[key].get("weight", 1.0)) + 0.1)
            else:
                existing_edges[key] = edge_d

        updated_extraction = {
            "nodes": list(existing_nodes.values()),
            "edges": list(existing_edges.values())
        }

        # Validate with Graphify
        GraphifyAdapter.assert_valid(updated_extraction)

        # Save to per-tenant store
        self.storage.save_graph_dict(user_id, updated_extraction)

        return {
            "status": "persisted",
            "nodes_added_or_updated": len(new_nodes_dict),
            "edges_added_or_updated": len(new_edges_dict),
            "total_nodes": len(existing_nodes),
            "total_edges": len(existing_edges)
        }
