from sqlalchemy import Column, String, Date, Boolean, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import BaseModel

class Participant(BaseModel):
    __tablename__ = "participants"
    participant_id = Column(String(20), unique=True, nullable=False, index=True)  # Pseudonymous ID
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    site_id = Column(String(36), ForeignKey("sites.id"), nullable=False, index=True)
    screening_date = Column(Date, nullable=True)
    enrollment_date = Column(Date, nullable=True)
    status = Column(String(20), default="SCREENED", index=True)
    # SCREENED, ELIGIBLE, CONSENTED, ENROLLED, RANDOMIZED, ACTIVE, COMPLETED, WITHDRAWN
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)
    
    trial = relationship("Trial")
    site = relationship("Site")
    consents = relationship("Consent", back_populates="participant", lazy="selectin")
    visits = relationship("ParticipantVisit", back_populates="participant", lazy="selectin")
    adverse_events = relationship("AdverseEvent", back_populates="participant", lazy="selectin")

class Consent(BaseModel):
    __tablename__ = "consents"
    participant_id = Column(String(36), ForeignKey("participants.id"), nullable=False, index=True)
    consent_type = Column(String(50), default="INFORMED_CONSENT")
    consent_date = Column(Date, nullable=False)
    consent_version = Column(String(20), nullable=True)
    consented_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    witness_name = Column(String(255), nullable=True)
    withdrawn = Column(Boolean, default=False)
    withdrawal_date = Column(Date, nullable=True)
    withdrawal_reason = Column(Text, nullable=True)
    
    participant = relationship("Participant", back_populates="consents")

class Screening(BaseModel):
    __tablename__ = "screenings"
    participant_id = Column(String(36), ForeignKey("participants.id"), nullable=False, index=True)
    screening_date = Column(Date, nullable=False)
    eligible = Column(Boolean, nullable=True)
    ineligibility_reason = Column(Text, nullable=True)
    screened_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)
    
    participant = relationship("Participant")

class Enrollment(BaseModel):
    __tablename__ = "enrollments"
    participant_id = Column(String(36), ForeignKey("participants.id"), nullable=False, unique=True)
    enrollment_date = Column(Date, nullable=False)
    enrolled_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    enrollment_number = Column(String(20), nullable=True)
    
    participant = relationship("Participant")

class Randomization(BaseModel):
    __tablename__ = "randomizations"
    participant_id = Column(String(36), ForeignKey("participants.id"), nullable=False, unique=True)
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False)
    randomization_date = Column(Date, nullable=False)
    randomization_number = Column(String(20), nullable=True)
    assigned_arm_id = Column(String(36), ForeignKey("study_arms.id"), nullable=True)
    assigned_arm_name = Column(String(100), nullable=True)
    randomized_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    is_locked = Column(Boolean, default=True)
    
    participant = relationship("Participant")
    arm = relationship("StudyArm")

class Withdrawal(BaseModel):
    __tablename__ = "withdrawals"
    participant_id = Column(String(36), ForeignKey("participants.id"), nullable=False, index=True)
    withdrawal_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=True)
    withdrawn_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)
    
    participant = relationship("Participant")
