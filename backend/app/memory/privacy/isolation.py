import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
import networkx as nx

from app.memory.graph.storage import TenantGraphStorage
from app.memory.graph.adapter import GraphifyAdapter
from app.memory.types.models import ForgetResponse, AuditRecord, MemoryNode

logger = logging.getLogger(__name__)

class MemoryPrivacyManager:
    """
    Handles multi-tenant isolation, privacy safety, provenance auditing, decay, and forgetting.
    """

    def __init__(self, storage: Optional[TenantGraphStorage] = None):
        self.storage = storage or TenantGraphStorage()

    def verify_tenant_access(self, requesting_user_id: str, target_user_id: str) -> None:
        """Enforce strict cross-tenant memory isolation."""
        if requesting_user_id != target_user_id and requesting_user_id != "admin":
            raise PermissionError(f"Access denied: User {requesting_user_id} cannot access memory of user {target_user_id}")

    def forget_user_memories(
        self,
        user_id: str,
        topic: Optional[str] = None,
        entity_type: Optional[str] = None,
        clear_all: bool = False
    ) -> ForgetResponse:
        """User-requested forgetting API."""
        if clear_all:
            graph_dict = self.storage.load_graph_dict(user_id)
            deleted_nodes = len(graph_dict.get("nodes", []))
            deleted_edges = len(graph_dict.get("edges", []))
            deleted = self.storage.delete_tenant_graph(user_id)
            return ForgetResponse(
                deleted_nodes=deleted_nodes if deleted else 0,
                deleted_edges=deleted_edges if deleted else 0,
                status="success",
                message=f"All memory for user {user_id} has been completely deleted."
            )

        graph_dict = self.storage.load_graph_dict(user_id)
        nodes = graph_dict.get("nodes", [])
        edges = graph_dict.get("edges", [])

        nodes_to_keep = []
        deleted_node_ids = set()

        for n in nodes:
            should_delete = False
            if topic and topic.lower() in str(n.get("label", "")).lower():
                should_delete = True
            if entity_type and n.get("entity_type") == entity_type:
                should_delete = True
            
            if should_delete:
                deleted_node_ids.add(n["id"])
            else:
                nodes_to_keep.append(n)

        edges_to_keep = []
        deleted_edge_count = 0
        for e in edges:
            if e["source"] in deleted_node_ids or e["target"] in deleted_node_ids:
                deleted_edge_count += 1
            else:
                edges_to_keep.append(e)

        updated_dict = {"nodes": nodes_to_keep, "edges": edges_to_keep}
        self.storage.save_graph_dict(user_id, updated_dict)

        return ForgetResponse(
            deleted_nodes=len(deleted_node_ids),
            deleted_edges=deleted_edge_count,
            status="success",
            message=f"Forgot {len(deleted_node_ids)} nodes and {deleted_edge_count} edges for user {user_id}."
        )

    def apply_confidence_decay(self, user_id: str, min_confidence: float = 0.2) -> Dict[str, Any]:
        """Decay confidence scores of old memories and mark low confidence ones as stale."""
        graph_dict = self.storage.load_graph_dict(user_id)
        if not graph_dict.get("nodes"):
            return {"updated_nodes": 0, "stale_marked": 0}

        graph = GraphifyAdapter.build_graph([graph_dict])
        now = datetime.utcnow()
        stale_count = 0
        updated_count = 0

        for n, attrs in graph.nodes(data=True):
            updated_at_str = attrs.get("updated_at") or attrs.get("created_at")
            if not updated_at_str:
                continue

            try:
                dt = datetime.fromisoformat(updated_at_str.replace("Z", "+00:00")).replace(tzinfo=None)
                age_days = (now - dt).total_seconds() / 86400.0
                if age_days > 14:  # older than 2 weeks
                    current_conf = float(attrs.get("confidence_score", 1.0))
                    new_conf = max(0.0, current_conf * 0.9)
                    attrs["confidence_score"] = new_conf
                    updated_count += 1
                    if new_conf < min_confidence:
                        attrs["is_stale"] = True
                        stale_count += 1
            except Exception:
                pass

        updated_graph_dict = GraphifyAdapter.graph_to_extraction_dict(graph, user_id)
        self.storage.save_graph_dict(user_id, updated_graph_dict)

        return {"updated_nodes": updated_count, "stale_marked": stale_count}

    def merge_duplicate_memories(
        self, user_id: str, primary_node_id: str, duplicate_node_ids: List[str]
    ) -> Dict[str, Any]:
        """Merge duplicate nodes into a primary node."""
        graph_dict = self.storage.load_graph_dict(user_id)
        if not graph_dict.get("nodes"):
            return {"merged": False, "reason": "No graph found"}

        graph = GraphifyAdapter.build_graph([graph_dict])
        if not graph.has_node(primary_node_id):
            return {"merged": False, "reason": "Primary node not found"}

        for dup_id in duplicate_node_ids:
            if not graph.has_node(dup_id) or dup_id == primary_node_id:
                continue

            # Redirect edges from dup_id to primary_node_id
            for u, v, attrs in list(graph.in_edges(dup_id, data=True)):
                if u != primary_node_id:
                    graph.add_edge(u, primary_node_id, **attrs)
            for u, v, attrs in list(graph.out_edges(dup_id, data=True)):
                if v != primary_node_id:
                    graph.add_edge(primary_node_id, v, **attrs)

            graph.remove_node(dup_id)

        updated_dict = GraphifyAdapter.graph_to_extraction_dict(graph, user_id)
        self.storage.save_graph_dict(user_id, updated_dict)

        return {"merged": True, "primary_id": primary_node_id, "merged_count": len(duplicate_node_ids)}
