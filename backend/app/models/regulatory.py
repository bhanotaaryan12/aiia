from sqlalchemy import Column, String, Date, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class RegulatoryRecord(BaseModel):
    __tablename__ = "regulatory_records"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    record_type = Column(String(20), default="CTRI")  # CTRI, DCGI, IEC, OTHER
    registration_number = Column(String(50), nullable=True)
    submission_date = Column(Date, nullable=True)
    registration_date = Column(Date, nullable=True)
    status = Column(String(30), default="NOT_STARTED", index=True)
    # NOT_STARTED, PREPARING, SUBMITTED, UNDER_REVIEW, REGISTERED, UPDATE_REQUIRED, COMPLETED
    last_verified_date = Column(Date, nullable=True)
    responsible_officer_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)
    
    trial = relationship("Trial")
    officer = relationship("User", foreign_keys=[responsible_officer_id])

class RegulatoryChecklist(BaseModel):
    __tablename__ = "regulatory_checklists"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    category = Column(String(30), default="NDCT_RULES_2019")  # NDCT_RULES_2019, GCP, ICH
    item_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)
    completed_date = Column(Date, nullable=True)
    completed_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    evidence_document_id = Column(String(36), ForeignKey("documents.id", use_alter=True), nullable=True)
    notes = Column(Text, nullable=True)
    
    trial = relationship("Trial")
