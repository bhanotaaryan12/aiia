from sqlalchemy import Column, String, Integer, Date, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import BaseModel

class Trial(BaseModel):
    __tablename__ = "trials"
    title = Column(String(500), nullable=False)
    short_title = Column(String(100), nullable=True)
    protocol_number = Column(String(50), unique=True, nullable=True, index=True)
    registration_number = Column(String(50), nullable=True)
    phase = Column(String(20), nullable=True)  # Phase 1, Phase 2, Phase 3, Phase 4
    study_type = Column(String(50), nullable=True)  # Interventional, Observational
    intervention_type = Column(String(50), nullable=True)
    therapeutic_area = Column(String(100), nullable=True)
    ayurveda_system = Column(String(100), nullable=True)
    primary_objective = Column(Text, nullable=True)
    secondary_objectives = Column(Text, nullable=True)
    inclusion_criteria = Column(Text, nullable=True)
    exclusion_criteria = Column(Text, nullable=True)
    planned_sample_size = Column(Integer, nullable=True)
    sponsor = Column(String(255), nullable=True)
    pi_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    start_date = Column(Date, nullable=True)
    expected_end_date = Column(Date, nullable=True)
    actual_end_date = Column(Date, nullable=True)
    status = Column(String(30), default="PLANNING", index=True)
    # PLANNING, ETHICS_PENDING, ETHICS_APPROVED, REGULATORY_PENDING, REGISTERED, RECRUITING, ACTIVE, COMPLETED, SUSPENDED, TERMINATED
    description = Column(Text, nullable=True)
    
    pi = relationship("User", foreign_keys=[pi_id])
    study_arms = relationship("StudyArm", back_populates="trial", lazy="selectin")
    interventions = relationship("Intervention", back_populates="trial", lazy="selectin")
    milestones = relationship("TrialMilestone", back_populates="trial", lazy="selectin")
    sites = relationship("SiteAssignment", back_populates="trial", lazy="selectin")

class Protocol(BaseModel):
    __tablename__ = "protocols"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    version = Column(String(20), nullable=False)
    title = Column(String(500), nullable=True)
    document_url = Column(String(500), nullable=True)
    effective_date = Column(Date, nullable=True)
    status = Column(String(20), default="DRAFT")  # DRAFT, ACTIVE, SUPERSEDED
    
    trial = relationship("Trial")

class StudyArm(BaseModel):
    __tablename__ = "study_arms"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    allocation_ratio = Column(Float, default=1.0)
    arm_type = Column(String(30), default="TREATMENT")  # TREATMENT, CONTROL, PLACEBO
    
    trial = relationship("Trial", back_populates="study_arms")

class Intervention(BaseModel):
    __tablename__ = "interventions"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    type = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    dosage = Column(String(200), nullable=True)
    duration = Column(String(100), nullable=True)
    formulation = Column(String(200), nullable=True)
    
    trial = relationship("Trial", back_populates="interventions")

class TrialMilestone(BaseModel):
    __tablename__ = "trial_milestones"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    planned_date = Column(Date, nullable=True)
    actual_date = Column(Date, nullable=True)
    status = Column(String(20), default="PENDING")  # PENDING, COMPLETED, DELAYED
    notes = Column(Text, nullable=True)
    
    trial = relationship("Trial", back_populates="milestones")
