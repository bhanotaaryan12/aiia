import logging
from typing import List, Dict, Any, Set, Tuple
import networkx as nx

from app.memory.types.enums import EntityType, MemoryType
from app.memory.types.models import MemoryNode, MemoryEdge
from app.memory.graph.adapter import GraphifyAdapter

logger = logging.getLogger(__name__)

class GraphSearch:
    """
    Search and graph traversal methods on NetworkX graphs.
    """

    @classmethod
    def find_seed_nodes(cls, graph: nx.Graph, query: str, user_id: str) -> List[str]:
        """
        Find seed nodes matching words in the query or user anchor.
        """
        query_words = set(w.lower() for w in query.split() if len(w) > 2)
        seed_ids = set()

        # Always include main user node if present
        user_main = f"{user_id}:user:main"
        if graph.has_node(user_main):
            seed_ids.add(user_main)

        for n, attrs in graph.nodes(data=True):
            if attrs.get("user_id") != user_id:
                continue
            
            label = str(attrs.get("label", "")).lower()
            node_id = str(n).lower()
            props = str(attrs.get("properties", "")).lower()

            for word in query_words:
                if word in label or word in node_id or word in props:
                    seed_ids.add(str(n))
                    break

        return list(seed_ids)

    @classmethod
    def get_subgraph_nodes(
        cls, graph: nx.Graph, seed_node_ids: List[str], max_hops: int = 2
    ) -> Set[str]:
        """
        Perform BFS traversal up to max_hops from seed nodes.
        """
        visited = set(seed_node_ids)
        current_layer = set(seed_node_ids)

        for _ in range(max_hops):
            next_layer = set()
            for node in current_layer:
                if not graph.has_node(node):
                    continue
                for neighbor in graph.neighbors(node):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        next_layer.add(neighbor)
            current_layer = next_layer
            if not current_layer:
                break

        return visited
