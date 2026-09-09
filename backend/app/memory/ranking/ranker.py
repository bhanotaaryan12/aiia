import math
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Tuple
import networkx as nx

from app.memory.types.models import MemoryNode

logger = logging.getLogger(__name__)

class MultiFactorRanker:
    """
    Ranks memory nodes using relevance, proximity, confidence, and recency.
    """

    @classmethod
    def calculate_recency_score(cls, timestamp_str: str, half_life_days: float = 30.0) -> float:
        """Exponential decay based on timestamp age."""
        if not timestamp_str:
            return 0.5
        try:
            dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            now = datetime.now(timezone.utc)
            age_days = (now - dt).total_seconds() / 86400.0
            if age_days < 0:
                age_days = 0
            return math.exp(-math.log(2) * (age_days / half_life_days))
        except Exception:
            return 0.5

    @classmethod
    def rank_nodes(
        cls,
        graph: nx.Graph,
        candidate_node_ids: List[str],
        seed_node_ids: List[str],
        query: str,
        weights: Tuple[float, float, float, float] = (0.4, 0.3, 0.2, 0.1)
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        Rank nodes and return list of (node_dict, composite_score) sorted descending.
        """
        w_rel, w_prox, w_conf, w_rec = weights
        scored_nodes = []

        query_terms = set(query.lower().split())

        for nid in candidate_node_ids:
            if not graph.has_node(nid):
                continue

            attrs = dict(graph.nodes[nid])

            # 1. Relevance score
            label = str(attrs.get("label", "")).lower()
            rel_score = 0.2
            if nid in seed_node_ids:
                rel_score = 0.9
            for t in query_terms:
                if len(t) > 2 and t in label:
                    rel_score = min(1.0, rel_score + 0.3)

            # 2. Proximity score (shortest path to any seed node)
            min_dist = float("inf")
            for seed in seed_node_ids:
                if graph.has_node(seed):
                    try:
                        d = nx.shortest_path_length(graph, source=seed, target=nid)
                        if d < min_dist:
                            min_dist = d
                    except nx.NetworkXNoPath:
                        pass
            if min_dist == float("inf"):
                prox_score = 0.1
            else:
                prox_score = 1.0 / (1.0 + min_dist)

            # 3. Confidence score
            conf_score = float(attrs.get("confidence_score", 1.0))

            # 4. Recency score
            rec_score = cls.calculate_recency_score(attrs.get("updated_at") or attrs.get("created_at"))

            composite = (w_rel * rel_score) + (w_prox * prox_score) + (w_conf * conf_score) + (w_rec * rec_score)
            
            # Penalize stale nodes
            if attrs.get("is_stale"):
                composite *= 0.3

            scored_nodes.append((attrs, composite))

        scored_nodes.sort(key=lambda x: x[1], reverse=True)
        return scored_nodes
