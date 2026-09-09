from pydantic import BaseModel
from typing import Optional
from datetime import date

class RegulatoryRecordCreate(BaseModel):
    trial_id: str
    record_type: str = "CTRI"
    registration_number: Optional[str] = None
    submission_date: Optional[date] = None
    status: str = "NOT_STARTED"
    notes: Optional[str] = None

class RegulatoryRecordUpdate(BaseModel):
    registration_number: Optional[str] = None
    submission_date: Optional[date] = None
    registration_date: Optional[date] = None
    status: Optional[str] = None
    last_verified_date: Optional[date] = None
    notes: Optional[str] = None

class RegulatoryChecklistCreate(BaseModel):
    trial_id: str
    category: str = "NDCT_RULES_2019"
    item_name: str
    description: Optional[str] = None

class RegulatoryChecklistUpdate(BaseModel):
    is_completed: Optional[bool] = None
    completed_date: Optional[date] = None
    notes: Optional[str] = None

class RegulatoryRecordOut(BaseModel):
    id: str
    trial_id: str
    record_type: str
    registration_number: Optional[str] = None
    submission_date: Optional[date] = None
    registration_date: Optional[date] = None
    status: str
    last_verified_date: Optional[date] = None
    notes: Optional[str] = None
    class Config:
        from_attributes = True

class RegulatoryChecklistOut(BaseModel):
    id: str
    trial_id: str
    category: str
    item_name: str
    description: Optional[str] = None
    is_completed: bool = False
    completed_date: Optional[date] = None
    notes: Optional[str] = None
    class Config:
        from_attributes = True
