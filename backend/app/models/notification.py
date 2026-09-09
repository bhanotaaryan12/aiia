from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from .base import BaseModel

class Notification(BaseModel):
    __tablename__ = "notifications"
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=True)
    type = Column(String(30), default="SYSTEM")
    # SAE_REPORTED, ETHICS_EXPIRING, REGULATORY_DEADLINE, OVERDUE_VISIT, DATA_QUERY, PROTOCOL_DEVIATION, SYSTEM
    entity_type = Column(String(50), nullable=True)
    entity_id = Column(String(36), nullable=True)
    is_read = Column(Boolean, default=False, index=True)
    read_at = Column(DateTime, nullable=True)
    priority = Column(String(10), default="NORMAL")  # LOW, NORMAL, HIGH, URGENT
