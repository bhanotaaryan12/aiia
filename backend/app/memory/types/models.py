from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from datetime import datetime, timezone
from app.memory.types.enums import EntityType, RelationType, MemoryType, ConfidenceLevel

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

class Provenance(BaseModel):
    source_message_id: Optional[str] = None
    session_id: Optional[str] = None
    extracted_by: str = "system"
    timestamp: str = Field(default_factory=utc_now_iso)
    raw_text: Optional[str] = None

class MemoryNode(BaseModel):
    id: str
    label: str
    entity_type: EntityType
    memory_type: MemoryType = MemoryType.LONG_TERM_SEMANTIC
    confidence_score: float = Field(default=1.0, ge=0.0, le=1.0)
    confidence: ConfidenceLevel = ConfidenceLevel.EXTRACTED
    user_id: str
    created_at: str = Field(default_factory=utc_now_iso)
    updated_at: str = Field(default_factory=utc_now_iso)
    is_stale: bool = False
    sensitive_flag: bool = False
    provenance: Optional[Provenance] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    
    # Graphify strict schema requirements
    file_type: str = "concept"
    source_file: str = "memory://concept"

    def to_graphify_dict(self) -> Dict[str, Any]:
        """Convert to dictionary matching Graphify node schema exactly."""
        d = {
            "id": self.id,
            "label": self.label,
            "file_type": self.file_type,
            "source_file": self.source_file if self.source_file else f"memory://{self.user_id}/{self.entity_type.value.lower()}",
            "entity_type": self.entity_type.value,
            "memory_type": self.memory_type.value,
            "confidence_score": self.confidence_score,
            "confidence": self.confidence.value,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_stale": self.is_stale,
            "sensitive_flag": self.sensitive_flag,
            "properties": self.properties,
        }
        if self.provenance:
            d["provenance"] = self.provenance.model_dump()
        return d

    @classmethod
    def from_graphify_dict(cls, data: Dict[str, Any]) -> "MemoryNode":
        provenance = Provenance(**data["provenance"]) if "provenance" in data and isinstance(data["provenance"], dict) else None
        return cls(
            id=data["id"],
            label=data["label"],
            entity_type=EntityType(data.get("entity_type", EntityType.TOPIC.value)),
            memory_type=MemoryType(data.get("memory_type", MemoryType.LONG_TERM_SEMANTIC.value)),
            confidence_score=float(data.get("confidence_score", 1.0)),
            confidence=ConfidenceLevel(data.get("confidence", ConfidenceLevel.EXTRACTED.value)),
            user_id=data.get("user_id", "system"),
            created_at=data.get("created_at", utc_now_iso()),
            updated_at=data.get("updated_at", utc_now_iso()),
            is_stale=data.get("is_stale", False),
            sensitive_flag=data.get("sensitive_flag", False),
            provenance=provenance,
            properties=data.get("properties", {}),
            file_type=data.get("file_type", "concept"),
            source_file=data.get("source_file", "memory://concept"),
        )

class MemoryEdge(BaseModel):
    source: str
    target: str
    relation: RelationType
    confidence: ConfidenceLevel = ConfidenceLevel.EXTRACTED
    weight: float = Field(default=1.0, ge=0.0)
    user_id: str
    created_at: str = Field(default_factory=utc_now_iso)
    updated_at: str = Field(default_factory=utc_now_iso)
    provenance: Optional[Provenance] = None
    source_file: str = "memory://relationships"

    def to_graphify_dict(self) -> Dict[str, Any]:
        """Convert to dictionary matching Graphify edge schema exactly."""
        d = {
            "source": self.source,
            "target": self.target,
            "relation": self.relation.value if isinstance(self.relation, RelationType) else str(self.relation),
            "confidence": self.confidence.value if isinstance(self.confidence, ConfidenceLevel) else str(self.confidence),
            "source_file": self.source_file if self.source_file else f"memory://{self.user_id}/relationships",
            "weight": self.weight,
            "user_id": self.user_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }
        if self.provenance:
            d["provenance"] = self.provenance.model_dump()
        return d

    @classmethod
    def from_graphify_dict(cls, data: Dict[str, Any]) -> "MemoryEdge":
        provenance = Provenance(**data["provenance"]) if "provenance" in data and isinstance(data["provenance"], dict) else None
        return cls(
            source=data["source"],
            target=data["target"],
            relation=RelationType(data.get("relation", RelationType.RELATED_TO.value)),
            confidence=ConfidenceLevel(data.get("confidence", ConfidenceLevel.EXTRACTED.value)),
            weight=float(data.get("weight", 1.0)),
            user_id=data.get("user_id", "system"),
            created_at=data.get("created_at", utc_now_iso()),
            updated_at=data.get("updated_at", utc_now_iso()),
            provenance=provenance,
            source_file=data.get("source_file", "memory://relationships"),
        )

class ExtractionResult(BaseModel):
    nodes: List[MemoryNode]
    edges: List[MemoryEdge]
    summary: str = ""

class ContextPackage(BaseModel):
    user: Dict[str, Any] = Field(default_factory=dict)
    relevant_facts: List[Dict[str, Any]] = Field(default_factory=list)
    preferences: List[Dict[str, Any]] = Field(default_factory=list)
    recent_events: List[Dict[str, Any]] = Field(default_factory=list)
    related_entities: List[Dict[str, Any]] = Field(default_factory=list)
    active_projects: List[Dict[str, Any]] = Field(default_factory=list)
    conversation_context: List[Dict[str, Any]] = Field(default_factory=list)
    confidence: Dict[str, float] = Field(default_factory=dict)

class AuditRecord(BaseModel):
    timestamp: str = Field(default_factory=utc_now_iso)
    user_id: str
    action: str
    target_id: str
    details: Dict[str, Any] = Field(default_factory=dict)

class ForgetResponse(BaseModel):
    deleted_nodes: int
    deleted_edges: int
    status: str = "success"
    message: str = ""
