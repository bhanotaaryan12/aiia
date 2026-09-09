from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class ParticipantCreate(BaseModel):
    trial_id: str
    site_id: str
    age: Optional[int] = None
    gender: Optional[str] = None

class ParticipantUpdate(BaseModel):
    status: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None

class ParticipantOut(BaseModel):
    id: str
    participant_id: str
    trial_id: str
    site_id: str
    screening_date: Optional[date] = None
    enrollment_date: Optional[date] = None
    status: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class ConsentCreate(BaseModel):
    participant_id: str
    consent_date: date
    consent_version: Optional[str] = None
    witness_name: Optional[str] = None

class ScreeningCreate(BaseModel):
    participant_id: str
    screening_date: date
    eligible: Optional[bool] = None
    ineligibility_reason: Optional[str] = None

class EnrollmentCreate(BaseModel):
    participant_id: str
    enrollment_date: date

class RandomizationOut(BaseModel):
    id: str
    participant_id: str
    randomization_date: Optional[date] = None
    randomization_number: Optional[str] = None
    assigned_arm_name: Optional[str] = None
    is_locked: bool = True
    class Config:
        from_attributes = True
