from enum import Enum

class EntityType(str, Enum):
    USER = "User"
    PERSON = "Person"
    ORGANIZATION = "Organization"
    PROJECT = "Project"
    TOPIC = "Topic"
    PREFERENCE = "Preference"
    FACT = "Fact"
    EVENT = "Event"
    CONVERSATION = "Conversation"
    TASK = "Task"
    DOCUMENT = "Document"

class RelationType(str, Enum):
    KNOWS = "KNOWS"
    PREFERS = "PREFERS"
    WORKS_ON = "WORKS_ON"
    RELATED_TO = "RELATED_TO"
    MENTIONED_IN = "MENTIONED_IN"
    DEPENDS_ON = "DEPENDS_ON"
    OCCURRED_AT = "OCCURRED_AT"
    BELONGS_TO = "BELONGS_TO"
    UPDATED_BY = "UPDATED_BY"

class MemoryType(str, Enum):
    SHORT_TERM = "short_term"
    LONG_TERM_SEMANTIC = "long_term_semantic"
    USER_PREFERENCE = "user_preference"
    EPISODIC = "episodic"
    EXPLICIT_FACT = "explicit_fact"

class ConfidenceLevel(str, Enum):
    EXTRACTED = "EXTRACTED"
    INFERRED = "INFERRED"
    AMBIGUOUS = "AMBIGUOUS"
