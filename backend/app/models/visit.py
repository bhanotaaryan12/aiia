from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class VisitDefinition(BaseModel):
    __tablename__ = "visit_definitions"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    visit_name = Column(String(100), nullable=False)
    visit_number = Column(Integer, nullable=False)
    visit_type = Column(String(30), default="TREATMENT")
    # SCREENING, BASELINE, TREATMENT, FOLLOW_UP, END_OF_STUDY
    day_offset = Column(Integer, default=0)
    window_before = Column(Integer, default=3)
    window_after = Column(Integer, default=3)
    is_required = Column(Boolean, default=True)
    
    trial = relationship("Trial")

class ParticipantVisit(BaseModel):
    __tablename__ = "participant_visits"
    participant_id = Column(String(36), ForeignKey("participants.id"), nullable=False, index=True)
    visit_definition_id = Column(String(36), ForeignKey("visit_definitions.id"), nullable=True)
    visit_name = Column(String(100), nullable=True)
    scheduled_date = Column(Date, nullable=True)
    actual_date = Column(Date, nullable=True)
    status = Column(String(20), default="SCHEDULED", index=True)
    # SCHEDULED, COMPLETED, MISSED, OVERDUE, CANCELLED
    notes = Column(Text, nullable=True)
    completed_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    
    participant = relationship("Participant", back_populates="visits")
    visit_definition = relationship("VisitDefinition")
