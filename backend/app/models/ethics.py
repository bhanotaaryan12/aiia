from sqlalchemy import Column, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class EthicsCommittee(BaseModel):
    __tablename__ = "ethics_committees"
    name = Column(String(255), nullable=False)
    institution = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    registration_number = Column(String(50), nullable=True)
    chairperson = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)

class EthicsSubmission(BaseModel):
    __tablename__ = "ethics_submissions"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    committee_id = Column(String(36), ForeignKey("ethics_committees.id"), nullable=True)
    submission_type = Column(String(30), default="INITIAL")
    # INITIAL, AMENDMENT, RENEWAL, SAE_REPORT
    submission_date = Column(Date, nullable=True)
    status = Column(String(30), default="DRAFT", index=True)
    # DRAFT, SUBMITTED, UNDER_REVIEW, CLARIFICATION_REQUIRED, APPROVED, REJECTED
    submitted_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    title = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    
    trial = relationship("Trial")
    committee = relationship("EthicsCommittee")
    reviews = relationship("EthicsReview", back_populates="submission", lazy="selectin")
    approval = relationship("EthicsApproval", back_populates="submission", uselist=False, lazy="selectin")

class EthicsReview(BaseModel):
    __tablename__ = "ethics_reviews"
    submission_id = Column(String(36), ForeignKey("ethics_submissions.id"), nullable=False, index=True)
    reviewer = Column(String(255), nullable=True)
    review_date = Column(Date, nullable=True)
    decision = Column(String(30), nullable=True)  # APPROVED, REJECTED, REVISIONS_REQUIRED
    comments = Column(Text, nullable=True)
    conditions = Column(Text, nullable=True)
    
    submission = relationship("EthicsSubmission", back_populates="reviews")

class EthicsApproval(BaseModel):
    __tablename__ = "ethics_approvals"
    submission_id = Column(String(36), ForeignKey("ethics_submissions.id"), nullable=False)
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False)
    approval_number = Column(String(50), nullable=True)
    approval_date = Column(Date, nullable=True)
    valid_from = Column(Date, nullable=True)
    valid_until = Column(Date, nullable=True)
    conditions = Column(Text, nullable=True)
    document_url = Column(String(500), nullable=True)
    
    submission = relationship("EthicsSubmission", back_populates="approval")
    trial = relationship("Trial")

class ProtocolAmendment(BaseModel):
    __tablename__ = "protocol_amendments"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    amendment_number = Column(String(20), nullable=False)
    description = Column(Text, nullable=True)
    submission_date = Column(Date, nullable=True)
    approval_date = Column(Date, nullable=True)
    status = Column(String(20), default="DRAFT")  # DRAFT, SUBMITTED, APPROVED, REJECTED
    changes_summary = Column(Text, nullable=True)
    
    trial = relationship("Trial")
