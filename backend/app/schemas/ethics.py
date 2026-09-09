from pydantic import BaseModel
from typing import Optional
from datetime import date

class EthicsCommitteeCreate(BaseModel):
    name: str
    institution: Optional[str] = None
    registration_number: Optional[str] = None
    chairperson: Optional[str] = None
    contact_email: Optional[str] = None

class EthicsSubmissionCreate(BaseModel):
    trial_id: str
    committee_id: Optional[str] = None
    submission_type: str = "INITIAL"
    title: Optional[str] = None
    description: Optional[str] = None

class EthicsSubmissionUpdate(BaseModel):
    status: Optional[str] = None
    submission_date: Optional[date] = None

class EthicsApprovalCreate(BaseModel):
    submission_id: str
    trial_id: str
    approval_number: Optional[str] = None
    approval_date: Optional[date] = None
    valid_from: Optional[date] = None
    valid_until: Optional[date] = None
    conditions: Optional[str] = None

class EthicsSubmissionOut(BaseModel):
    id: str
    trial_id: str
    submission_type: str
    submission_date: Optional[date] = None
    status: str
    title: Optional[str] = None
    description: Optional[str] = None
    class Config:
        from_attributes = True

class EthicsApprovalOut(BaseModel):
    id: str
    trial_id: str
    approval_number: Optional[str] = None
    approval_date: Optional[date] = None
    valid_from: Optional[date] = None
    valid_until: Optional[date] = None
    conditions: Optional[str] = None
    class Config:
        from_attributes = True

class EthicsCommitteeOut(BaseModel):
    id: str
    name: str
    institution: Optional[str] = None
    registration_number: Optional[str] = None
    class Config:
        from_attributes = True
