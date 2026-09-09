import re
import uuid
import logging
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional, Tuple

from app.memory.types.enums import EntityType, RelationType, MemoryType, ConfidenceLevel
from app.memory.types.models import MemoryNode, MemoryEdge, Provenance, ExtractionResult

logger = logging.getLogger(__name__)

class MemoryExtractionPipeline:
    """
    Extracts entities, preferences, facts, events, and relationships from text or chat history.
    Enforces rules:
    - Explicit user statements get MemoryType.EXPLICIT_FACT and ConfidenceLevel.EXTRACTED.
    - Inferred statements get MemoryType.LONG_TERM_SEMANTIC and ConfidenceLevel.INFERRED.
    - Deduplicates entities by canonical key.
    """

    PREFERENCE_PATTERNS = [
        r"(?:i prefer|i like|i want|my preference is|always show me|please use)\s+(.+)",
        r"(?:prefer|like|want)\s+(.+)\s+over\s+(.+)",
    ]

    FACT_PATTERNS = [
        (r"(?:my name is|i am)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)", EntityType.FACT, "user_name", re.IGNORECASE),
        (r"(?:i work at|i am affiliated with)\s+([A-Z][a-zA-Z0-9\s]+)", EntityType.ORGANIZATION, "affiliation", re.IGNORECASE),
        (r"(?:project|trial|study)\s+([A-Z0-9_]+-[A-Z0-9_\-]+)", EntityType.PROJECT, "project_name", 0),
        (r"(?:i work on|i am working on|my project is|current project is)\s+([A-Z0-9_\-]+)", EntityType.PROJECT, "project_name", re.IGNORECASE),
    ]

    TOPIC_KEYWORDS = {
        "ashwagandha": ("Ashwagandha", "Ayurvedic Herbal Formulation"),
        "shatavari": ("Shatavari", "Ayurvedic Herbal Formulation"),
        "curcumin": ("Curcumin", "Bioactive Compound"),
        "diabetes": ("Type 2 Diabetes Mellitus", "Medical Condition"),
        "osteoarthritis": ("Osteoarthritis", "Medical Condition"),
        "ndct": ("NDCT Rules 2019", "Regulatory Framework"),
        "cdisc": ("CDISC Standards", "Data Standard"),
        "fhir": ("HL7 FHIR Interoperability", "Health Data Protocol"),
        "pharmacovigilance": ("Pharmacovigilance", "Safety Monitoring"),
    }

    def __init__(self):
        pass

    def _generate_canonical_id(self, user_id: str, entity_type: EntityType, label: str) -> str:
        clean_label = re.sub(r"[^a-zA-Z0-9]", "_", label.strip().lower())
        clean_label = re.sub(r"_+", "_", clean_label).strip("_")
        return f"{user_id}:{entity_type.value.lower()}:{clean_label}"

    def extract_from_message(
        self,
        user_id: str,
        message: str,
        role: str = "user",
        session_id: Optional[str] = None,
        source_message_id: Optional[str] = None
    ) -> ExtractionResult:
        """
        Extract entities, preferences, facts, and relationships from a message.
        """
        nodes: List[MemoryNode] = []
        edges: List[MemoryEdge] = []
        now_iso = datetime.now(timezone.utc).isoformat()

        prov = Provenance(
            source_message_id=source_message_id or str(uuid.uuid4())[:8],
            session_id=session_id or "default",
            extracted_by="rules_pipeline",
            timestamp=now_iso,
            raw_text=message
        )

        user_node_id = f"{user_id}:user:main"
        user_node = MemoryNode(
            id=user_node_id,
            label=f"User ({user_id})",
            entity_type=EntityType.USER,
            memory_type=MemoryType.LONG_TERM_SEMANTIC,
            confidence_score=1.0,
            confidence=ConfidenceLevel.EXTRACTED,
            user_id=user_id,
            created_at=now_iso,
            updated_at=now_iso,
            provenance=prov,
            properties={"role": role}
        )
        nodes.append(user_node)

        # 1. Preferences
        for pat in self.PREFERENCE_PATTERNS:
            match = re.search(pat, message, re.IGNORECASE)
            if match:
                pref_text = match.group(1).strip()
                pref_id = self._generate_canonical_id(user_id, EntityType.PREFERENCE, pref_text)
                pref_node = MemoryNode(
                    id=pref_id,
                    label=f"Preference: {pref_text}",
                    entity_type=EntityType.PREFERENCE,
                    memory_type=MemoryType.USER_PREFERENCE,
                    confidence_score=0.95,
                    confidence=ConfidenceLevel.EXTRACTED,
                    user_id=user_id,
                    created_at=now_iso,
                    updated_at=now_iso,
                    provenance=prov,
                    properties={"preference_detail": pref_text, "source": "explicit_user_statement"}
                )
                nodes.append(pref_node)
                edges.append(MemoryEdge(
                    source=user_node_id,
                    target=pref_id,
                    relation=RelationType.PREFERS,
                    confidence=ConfidenceLevel.EXTRACTED,
                    weight=1.0,
                    user_id=user_id,
                    created_at=now_iso,
                    updated_at=now_iso,
                    provenance=prov
                ))

        # 2. Facts and Projects
        for pat, ent_type, key_name, flags in self.FACT_PATTERNS:
            match = re.search(pat, message, flags)
            if match:
                val = match.group(1).strip()
                if val.lower() in ("project", "trial", "study", "status"):
                    continue
                node_id = self._generate_canonical_id(user_id, ent_type, val)
                
                rel = RelationType.WORKS_ON if ent_type == EntityType.PROJECT else RelationType.RELATED_TO
                m_type = MemoryType.EXPLICIT_FACT if ent_type == EntityType.FACT else MemoryType.LONG_TERM_SEMANTIC

                fact_node = MemoryNode(
                    id=node_id,
                    label=f"{ent_type.value}: {val}",
                    entity_type=ent_type,
                    memory_type=m_type,
                    confidence_score=0.95,
                    confidence=ConfidenceLevel.EXTRACTED,
                    user_id=user_id,
                    created_at=now_iso,
                    updated_at=now_iso,
                    provenance=prov,
                    properties={key_name: val}
                )
                nodes.append(fact_node)
                edges.append(MemoryEdge(
                    source=user_node_id,
                    target=node_id,
                    relation=rel,
                    confidence=ConfidenceLevel.EXTRACTED,
                    weight=1.0,
                    user_id=user_id,
                    created_at=now_iso,
                    updated_at=now_iso,
                    provenance=prov
                ))

        # 3. Topic keywords
        lower_msg = message.lower()
        for kw, (topic_name, category) in self.TOPIC_KEYWORDS.items():
            if kw in lower_msg:
                topic_id = self._generate_canonical_id(user_id, EntityType.TOPIC, topic_name)
                topic_node = MemoryNode(
                    id=topic_id,
                    label=topic_name,
                    entity_type=EntityType.TOPIC,
                    memory_type=MemoryType.LONG_TERM_SEMANTIC,
                    confidence_score=0.85,
                    confidence=ConfidenceLevel.EXTRACTED,
                    user_id=user_id,
                    created_at=now_iso,
                    updated_at=now_iso,
                    provenance=prov,
                    properties={"category": category}
                )
                nodes.append(topic_node)
                edges.append(MemoryEdge(
                    source=user_node_id,
                    target=topic_id,
                    relation=RelationType.RELATED_TO,
                    confidence=ConfidenceLevel.EXTRACTED,
                    weight=0.8,
                    user_id=user_id,
                    created_at=now_iso,
                    updated_at=now_iso,
                    provenance=prov
                ))

        # 4. Short-term / Episodic conversation node
        conv_id = f"{user_id}:conversation:{session_id or 'default'}:{source_message_id or uuid.uuid4().hex[:6]}"
        conv_node = MemoryNode(
            id=conv_id,
            label=f"Conversation Turn: {message[:30]}...",
            entity_type=EntityType.CONVERSATION,
            memory_type=MemoryType.SHORT_TERM,
            confidence_score=1.0,
            confidence=ConfidenceLevel.EXTRACTED,
            user_id=user_id,
            created_at=now_iso,
            updated_at=now_iso,
            provenance=prov,
            properties={"message_content": message, "role": role}
        )
        nodes.append(conv_node)
        edges.append(MemoryEdge(
            source=user_node_id,
            target=conv_id,
            relation=RelationType.MENTIONED_IN,
            confidence=ConfidenceLevel.EXTRACTED,
            weight=0.5,
            user_id=user_id,
            created_at=now_iso,
            updated_at=now_iso,
            provenance=prov
        ))

        # Connect extracted entities to conversation turn
        for n in nodes:
            if n.id != user_node_id and n.id != conv_id:
                edges.append(MemoryEdge(
                    source=n.id,
                    target=conv_id,
                    relation=RelationType.MENTIONED_IN,
                    confidence=ConfidenceLevel.EXTRACTED,
                    weight=0.7,
                    user_id=user_id,
                    created_at=now_iso,
                    updated_at=now_iso,
                    provenance=prov
                ))

        return ExtractionResult(
            nodes=nodes,
            edges=edges,
            summary=f"Extracted {len(nodes)} nodes and {len(edges)} edges."
        )
