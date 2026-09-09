from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class SiteCreate(BaseModel):
    name: str
    institution: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: str = "India"
    pin_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    target_enrollment: Optional[int] = None

class SiteUpdate(BaseModel):
    name: Optional[str] = None
    institution: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None
    target_enrollment: Optional[int] = None

class SiteOut(BaseModel):
    id: str
    name: str
    institution: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    status: Optional[str] = None
    target_enrollment: Optional[int] = None
    activation_date: Optional[date] = None
    created_at: Optional[datetime] = None
    participant_count: int = 0
    class Config:
        from_attributes = True

class SiteAssignmentCreate(BaseModel):
    trial_id: str
    site_id: str
    pi_id: Optional[str] = None
    target_enrollment: Optional[int] = None

class InvestigatorCreate(BaseModel):
    site_id: str
    name: str
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    experience_years: Optional[int] = None
    gcp_trained: bool = False
    email: Optional[str] = None

class InvestigatorOut(BaseModel):
    id: str
    name: str
    site_id: str
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    experience_years: Optional[int] = None
    gcp_trained: bool = False
    class Config:
        from_attributes = True
