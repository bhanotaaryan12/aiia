from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from pydantic import BaseModel

from app.memory.context.builder import build_context
from app.memory.middleware.lifecycle import AgentMemoryLifecycle
from app.memory.privacy.isolation import MemoryPrivacyManager
from app.memory.graph.storage import TenantGraphStorage
from app.memory.graph.adapter import GraphifyAdapter
from app.api.v1.auth import get_current_user

router = APIRouter()
lifecycle = AgentMemoryLifecycle()
privacy_mgr = MemoryPrivacyManager()
storage = TenantGraphStorage()

class ContextRequest(BaseModel):
    user_id: str
    message: str
    session_id: Optional[str] = None

class IngestRequest(BaseModel):
    user_id: str
    message: str
    response_text: str = ""
    session_id: Optional[str] = None

class ForgetRequest(BaseModel):
    user_id: str
    topic: Optional[str] = None
    entity_type: Optional[str] = None
    clear_all: bool = False

class UpdateNodeRequest(BaseModel):
    label: Optional[str] = None
    confidence_score: Optional[float] = None
    is_stale: Optional[bool] = None
    properties: Optional[Dict[str, Any]] = None

@router.post("/context")
async def api_build_context(req: ContextRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    user_id = current_user.get("email", req.user_id)
    privacy_mgr.verify_tenant_access(user_id, req.user_id)
    return build_context(user_id=req.user_id, message=req.message)

@router.post("/ingest")
async def api_ingest_memory(req: IngestRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    user_id = current_user.get("email", req.user_id)
    privacy_mgr.verify_tenant_access(user_id, req.user_id)
    res = lifecycle.after_agent_turn(
        user_id=req.user_id,
        message=req.message,
        response_text=req.response_text,
        session_id=req.session_id
    )
    return res

@router.get("/nodes")
async def api_get_nodes(user_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    curr_email = current_user.get("email", user_id)
    privacy_mgr.verify_tenant_access(curr_email, user_id)
    graph_dict = storage.load_graph_dict(user_id)
    return graph_dict

@router.delete("/nodes/{node_id:path}")
async def api_delete_node(node_id: str, user_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    curr_email = current_user.get("email", user_id)
    privacy_mgr.verify_tenant_access(curr_email, user_id)
    
    graph_dict = storage.load_graph_dict(user_id)
    nodes = graph_dict.get("nodes", [])
    edges = graph_dict.get("edges", [])

    new_nodes = [n for n in nodes if n["id"] != node_id]
    new_edges = [e for e in edges if e["source"] != node_id and e["target"] != node_id]

    if len(nodes) == len(new_nodes):
        raise HTTPException(status_code=404, detail="Node not found")

    storage.save_graph_dict(user_id, {"nodes": new_nodes, "edges": new_edges})
    return {"status": "deleted", "node_id": node_id}

@router.post("/forget")
async def api_forget(req: ForgetRequest, current_user: Dict[str, Any] = Depends(get_current_user)):
    curr_email = current_user.get("email", req.user_id)
    privacy_mgr.verify_tenant_access(curr_email, req.user_id)
    res = privacy_mgr.forget_user_memories(
        user_id=req.user_id,
        topic=req.topic,
        entity_type=req.entity_type,
        clear_all=req.clear_all
    )
    return res.model_dump()

@router.post("/decay")
async def api_decay(user_id: str, current_user: Dict[str, Any] = Depends(get_current_user)):
    curr_email = current_user.get("email", user_id)
    privacy_mgr.verify_tenant_access(curr_email, user_id)
    res = privacy_mgr.apply_confidence_decay(user_id=user_id)
    return res
