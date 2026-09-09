from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class Document(BaseModel):
    __tablename__ = "documents"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    document_type = Column(String(30), default="OTHER")
    # PROTOCOL, CONSENT_FORM, ETHICS_APPROVAL, REGULATORY, INVESTIGATOR_BROCHURE, SAFETY_REPORT, OTHER
    file_name = Column(String(255), nullable=True)
    file_path = Column(String(500), nullable=True)
    file_size = Column(Integer, nullable=True)
    mime_type = Column(String(100), nullable=True)
    uploaded_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    version = Column(String(20), default="1.0")
    status = Column(String(20), default="ACTIVE")  # ACTIVE, ARCHIVED
    description = Column(Text, nullable=True)
    
    trial = relationship("Trial")
