import pytest
import os
import shutil
from pathlib import Path

from app.memory.types.enums import EntityType, RelationType, MemoryType, ConfidenceLevel
from app.memory.types.models import MemoryNode, MemoryEdge, Provenance
from app.memory.graph.storage import TenantGraphStorage
from app.memory.graph.adapter import GraphifyAdapter
from app.memory.extraction.pipeline import MemoryExtractionPipeline
from app.memory.context.builder import build_context
from app.memory.privacy.isolation import MemoryPrivacyManager
from app.memory.middleware.lifecycle import AgentMemoryLifecycle

TEST_DATA_DIR = Path("data/test_memory")

@pytest.fixture(autouse=True)
def setup_test_env():
    TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
    yield
    if TEST_DATA_DIR.exists():
        shutil.rmtree(TEST_DATA_DIR)

def test_graphify_adapter_validation_and_build():
    """Verify Graphify schema validation and NetworkX graph assembly."""
    user_node = MemoryNode(
        id="u1:user:main",
        label="User Main",
        entity_type=EntityType.USER,
        user_id="u1"
    )
    fact_node = MemoryNode(
        id="u1:fact:ashwa",
        label="Ashwagandha Usage",
        entity_type=EntityType.FACT,
        user_id="u1"
    )
    edge = MemoryEdge(
        source="u1:user:main",
        target="u1:fact:ashwa",
        relation=RelationType.RELATED_TO,
        user_id="u1"
    )
    
    ext_dict = {
        "nodes": [user_node.to_graphify_dict(), fact_node.to_graphify_dict()],
        "edges": [edge.to_graphify_dict()]
    }

    # Graphify validation
    errors = GraphifyAdapter.validate_extraction(ext_dict)
    assert len(errors) == 0

    # Build NetworkX graph via Graphify build
    graph = GraphifyAdapter.build_graph([ext_dict])
    assert graph.number_of_nodes() == 2
    assert graph.has_node("u1:fact:ashwa")

def test_extraction_pipeline_explicit_vs_inferred():
    """Verify explicit facts vs inferred preferences in extraction pipeline."""
    pipeline = MemoryExtractionPipeline()
    
    # Message with preference and explicit fact
    msg = "My name is Dr. Anita and I prefer bullet point summaries for Ashwagandha trial."
    res = pipeline.extract_from_message(user_id="user_anita", message=msg)

    nodes_by_type = {n.entity_type: n for n in res.nodes}
    assert EntityType.PREFERENCE in nodes_by_type
    pref_node = nodes_by_type[EntityType.PREFERENCE]
    assert pref_node.memory_type == MemoryType.USER_PREFERENCE
    assert pref_node.confidence == ConfidenceLevel.EXTRACTED

    fact_node = nodes_by_type[EntityType.FACT]
    assert fact_node.memory_type == MemoryType.EXPLICIT_FACT
    assert fact_node.confidence == ConfidenceLevel.EXTRACTED

def test_lifecycle_ingest_and_deduplication():
    """Verify context building, memory ingestion, and entity deduplication."""
    storage = TenantGraphStorage(data_dir=TEST_DATA_DIR)
    lifecycle = AgentMemoryLifecycle(storage=storage)
    user_id = "test_user_dedup"

    # Turn 1
    lifecycle.after_agent_turn(
        user_id=user_id,
        message="I work on project AIIA-2024-01.",
        response_text="Noted project AIIA-2024-01."
    )

    # Turn 2 - mentions same project
    lifecycle.after_agent_turn(
        user_id=user_id,
        message="Update on project AIIA-2024-01: enrollment complete.",
        response_text="Updated project status."
    )

    graph_dict = storage.load_graph_dict(user_id)
    proj_nodes = [n for n in graph_dict["nodes"] if n["entity_type"] == EntityType.PROJECT.value]
    
    # Should deduplicate and keep single project node
    assert len(proj_nodes) == 1
    assert proj_nodes[0]["id"] == "test_user_dedup:project:aiia_2024_01"

def test_build_context_format():
    """Verify build_context returns required 8-key structured context package."""
    storage = TenantGraphStorage(data_dir=TEST_DATA_DIR)
    lifecycle = AgentMemoryLifecycle(storage=storage)
    user_id = "test_user_ctx"

    lifecycle.after_agent_turn(
        user_id=user_id,
        message="I prefer table format and work on Ashwagandha trial.",
        response_text="Saved preferences."
    )

    ctx = build_context(user_id=user_id, message="Tell me about Ashwagandha", storage=storage)
    
    required_keys = [
        "user", "relevant_facts", "preferences", "recent_events",
        "related_entities", "active_projects", "conversation_context", "confidence"
    ]
    for key in required_keys:
        assert key in ctx

    assert len(ctx["preferences"]) >= 1
    assert len(ctx["related_entities"]) >= 1

def test_tenant_isolation():
    """Verify strict multi-tenant isolation (User A cannot access or leak to User B)."""
    storage = TenantGraphStorage(data_dir=TEST_DATA_DIR)
    privacy = MemoryPrivacyManager(storage=storage)
    lifecycle = AgentMemoryLifecycle(storage=storage)

    # User A memory
    lifecycle.after_agent_turn(
        user_id="user_a",
        message="Secret password preference is 12345 for User A",
        response_text="Ok"
    )

    # User B memory
    lifecycle.after_agent_turn(
        user_id="user_b",
        message="User B works on Shatavari",
        response_text="Ok"
    )

    # Verify context for User B does NOT contain User A's data
    ctx_b = build_context(user_id="user_b", message="password preference", storage=storage)
    for pref in ctx_b["preferences"]:
        assert "User A" not in str(pref)

    # Verify privacy manager blocks unauthorized cross-tenant access
    with pytest.raises(PermissionError):
        privacy.verify_tenant_access(requesting_user_id="user_b", target_user_id="user_a")

def test_forgetting_api():
    """Verify user-requested forgetting functionality."""
    storage = TenantGraphStorage(data_dir=TEST_DATA_DIR)
    privacy = MemoryPrivacyManager(storage=storage)
    lifecycle = AgentMemoryLifecycle(storage=storage)
    user_id = "user_forget"

    lifecycle.after_agent_turn(
        user_id=user_id,
        message="I like Ashwagandha and Shatavari",
        response_text="Saved"
    )

    res = privacy.forget_user_memories(user_id=user_id, topic="ashwagandha")
    assert res.deleted_nodes >= 1

    graph_dict = storage.load_graph_dict(user_id)
    ashwa_nodes = [n for n in graph_dict["nodes"] if "ashwagandha" in n["label"].lower()]
    assert len(ashwa_nodes) == 0
