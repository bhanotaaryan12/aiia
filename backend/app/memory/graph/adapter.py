import logging
from typing import List, Dict, Any, Optional, Tuple, Set
import networkx as nx

import graphify.build as gbuild
import graphify.validate as gval
from app.memory.types.models import MemoryNode, MemoryEdge
from app.memory.types.enums import EntityType, RelationType, MemoryType, ConfidenceLevel

logger = logging.getLogger(__name__)

class GraphifyAdapter:
    """
    Adapter encapsulating Graphify SDK / NetworkX graph operations.
    Keeps all direct Graphify imports isolated so the rest of the application
    depends only on standard domain interfaces.
    """

    @staticmethod
    def validate_extraction(extraction_dict: Dict[str, Any]) -> List[str]:
        """Validate extraction dict against Graphify's official schema."""
        return gval.validate_extraction(extraction_dict)

    @staticmethod
    def assert_valid(extraction_dict: Dict[str, Any]) -> None:
        """Raise ValueError if extraction dict violates Graphify schema."""
        gval.assert_valid(extraction_dict)

    @classmethod
    def build_graph(cls, extractions: List[Dict[str, Any]]) -> nx.Graph:
        """
        Build NetworkX graph using Graphify's official build mechanism.
        """
        for ext in extractions:
            errors = cls.validate_extraction(ext)
            if errors:
                logger.warning(f"Graphify extraction validation warnings: {errors}")
        
        # Call graphify.build.build
        return gbuild.build(extractions, directed=True, dedup=True)

    @classmethod
    def graph_to_extraction_dict(cls, graph: nx.Graph, user_id: str) -> Dict[str, Any]:
        """
        Export a NetworkX graph into Graphify-compliant extraction dict format.
        """
        nodes_list = []
        for n, attrs in graph.nodes(data=True):
            node_dict = {
                "id": str(n),
                "label": str(attrs.get("label", n)),
                "file_type": attrs.get("file_type", "concept"),
                "source_file": attrs.get("source_file", f"memory://{user_id}/concept"),
                "entity_type": attrs.get("entity_type", EntityType.TOPIC.value),
                "memory_type": attrs.get("memory_type", MemoryType.LONG_TERM_SEMANTIC.value),
                "confidence_score": float(attrs.get("confidence_score", 1.0)),
                "confidence": attrs.get("confidence", ConfidenceLevel.EXTRACTED.value),
                "user_id": attrs.get("user_id", user_id),
                "created_at": attrs.get("created_at", ""),
                "updated_at": attrs.get("updated_at", ""),
                "is_stale": bool(attrs.get("is_stale", False)),
                "sensitive_flag": bool(attrs.get("sensitive_flag", False)),
                "properties": attrs.get("properties", {}),
            }
            if "provenance" in attrs:
                node_dict["provenance"] = attrs["provenance"]
            nodes_list.append(node_dict)

        edges_list = []
        for u, v, attrs in graph.edges(data=True):
            edge_dict = {
                "source": str(u),
                "target": str(v),
                "relation": attrs.get("relation", RelationType.RELATED_TO.value),
                "confidence": attrs.get("confidence", ConfidenceLevel.EXTRACTED.value),
                "source_file": attrs.get("source_file", f"memory://{user_id}/relationships"),
                "weight": float(attrs.get("weight", 1.0)),
                "user_id": attrs.get("user_id", user_id),
                "created_at": attrs.get("created_at", ""),
                "updated_at": attrs.get("updated_at", ""),
            }
            if "provenance" in attrs:
                edge_dict["provenance"] = attrs["provenance"]
            edges_list.append(edge_dict)

        return {"nodes": nodes_list, "edges": edges_list}

    @classmethod
    def nodes_to_models(cls, nodes_dicts: List[Dict[str, Any]]) -> List[MemoryNode]:
        models = []
        for d in nodes_dicts:
            try:
                models.append(MemoryNode.from_graphify_dict(d))
            except Exception as e:
                logger.warning(f"Error parsing node dict {d.get('id')}: {e}")
        return models

    @classmethod
    def edges_to_models(cls, edges_dicts: List[Dict[str, Any]]) -> List[MemoryEdge]:
        models = []
        for d in edges_dicts:
            try:
                models.append(MemoryEdge.from_graphify_dict(d))
            except Exception as e:
                logger.warning(f"Error parsing edge dict {d.get('source')} -> {d.get('target')}: {e}")
        return models
