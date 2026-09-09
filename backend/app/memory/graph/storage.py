import os
import json
import hashlib
import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)

MEMORY_DATA_DIR = Path(os.getenv("MEMORY_DATA_DIR", "data/memory"))

class TenantGraphStorage:
    def __init__(self, data_dir: Path = MEMORY_DATA_DIR):
        self.data_dir = data_dir
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def _get_user_file(self, user_id: str) -> Path:
        safe_user_id = hashlib.sha256(user_id.encode("utf-8")).hexdigest()
        return self.data_dir / f"user_{safe_user_id}.json"

    def load_graph_dict(self, user_id: str) -> Dict[str, Any]:
        """Load tenant graph as extraction dict compliant with Graphify schema."""
        file_path = self._get_user_file(user_id)
        if not file_path.exists():
            return {"nodes": [], "edges": []}
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                if not isinstance(data, dict):
                    return {"nodes": [], "edges": []}
                if "nodes" not in data:
                    data["nodes"] = []
                if "edges" not in data:
                    data["edges"] = []
                return data
        except Exception as e:
            logger.error(f"Failed to load graph for user {user_id}: {e}")
            return {"nodes": [], "edges": []}

    def save_graph_dict(self, user_id: str, data: Dict[str, Any]) -> None:
        """Save tenant graph dict to file storage."""
        file_path = self._get_user_file(user_id)
        file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            logger.debug(f"Saved graph for user {user_id} ({len(data.get('nodes', []))} nodes, {len(data.get('edges', []))} edges)")
        except Exception as e:
            logger.error(f"Failed to save graph for user {user_id}: {e}")
            raise e

    def delete_tenant_graph(self, user_id: str) -> bool:
        """Delete storage file for a given user."""
        file_path = self._get_user_file(user_id)
        if file_path.exists():
            file_path.unlink()
            return True
        return False
