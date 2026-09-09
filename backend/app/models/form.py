from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel

class Form(BaseModel):
    __tablename__ = "forms"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    version = Column(String(20), default="1.0")
    status = Column(String(20), default="ACTIVE")  # DRAFT, ACTIVE, RETIRED
    visit_type = Column(String(30), nullable=True)
    
    trial = relationship("Trial")
    fields = relationship("FormField", back_populates="form", lazy="selectin", order_by="FormField.order_index")

class FormField(BaseModel):
    __tablename__ = "form_fields"
    form_id = Column(String(36), ForeignKey("forms.id"), nullable=False, index=True)
    field_name = Column(String(100), nullable=False)
    field_label = Column(String(255), nullable=False)
    field_type = Column(String(30), nullable=False)
    # TEXT, NUMBER, DATE, DATETIME, BOOLEAN, SINGLE_SELECT, MULTI_SELECT, LAB_VALUE
    is_required = Column(Boolean, default=False)
    validation_rules = Column(JSON, nullable=True)  # {"min": 0, "max": 200}
    options = Column(JSON, nullable=True)  # ["option1", "option2"]
    order_index = Column(Integer, default=0)
    cdisc_domain = Column(String(10), nullable=True)
    cdisc_variable = Column(String(20), nullable=True)
    unit = Column(String(30), nullable=True)
    
    form = relationship("Form", back_populates="fields")

class FormSubmission(BaseModel):
    __tablename__ = "form_submissions"
    form_id = Column(String(36), ForeignKey("forms.id"), nullable=False, index=True)
    participant_id = Column(String(36), ForeignKey("participants.id"), nullable=False, index=True)
    visit_id = Column(String(36), ForeignKey("participant_visits.id"), nullable=True)
    submitted_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    submitted_at = Column(DateTime, nullable=True)
    status = Column(String(20), default="DRAFT")  # DRAFT, SUBMITTED, VERIFIED, LOCKED
    data = Column(JSON, nullable=True)
    
    form = relationship("Form")
    participant = relationship("Participant")

class DataPoint(BaseModel):
    __tablename__ = "data_points"
    submission_id = Column(String(36), ForeignKey("form_submissions.id"), nullable=False, index=True)
    field_id = Column(String(36), ForeignKey("form_fields.id"), nullable=False)
    value = Column(Text, nullable=True)
    is_valid = Column(Boolean, default=True)
    validation_message = Column(Text, nullable=True)
    
    submission = relationship("FormSubmission")
    field = relationship("FormField")

class DataQuery(BaseModel):
    __tablename__ = "data_queries"
    submission_id = Column(String(36), ForeignKey("form_submissions.id"), nullable=False, index=True)
    field_id = Column(String(36), ForeignKey("form_fields.id"), nullable=True)
    query_text = Column(Text, nullable=False)
    query_type = Column(String(30), default="MANUAL")  # MANUAL, AUTO_VALIDATION
    status = Column(String(20), default="OPEN", index=True)  # OPEN, ANSWERED, RESOLVED, CLOSED
    raised_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    answered_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    answer_text = Column(Text, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    
    submission = relationship("FormSubmission")
