from pydantic import BaseModel
from typing import Optional
from datetime import date

class VisitDefinitionCreate(BaseModel):
    trial_id: str
    visit_name: str
    visit_number: int
    visit_type: str = "TREATMENT"
    day_offset: int = 0
    window_before: int = 3
    window_after: int = 3
    is_required: bool = True

class ParticipantVisitCreate(BaseModel):
    participant_id: str
    visit_definition_id: Optional[str] = None
    visit_name: Optional[str] = None
    scheduled_date: Optional[date] = None
    actual_date: Optional[date] = None
    status: str = "SCHEDULED"
    notes: Optional[str] = None

class ParticipantVisitUpdate(BaseModel):
    actual_date: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class VisitDefinitionOut(BaseModel):
    id: str
    trial_id: str
    visit_name: str
    visit_number: int
    visit_type: str
    day_offset: int = 0
    is_required: bool = True
    class Config:
        from_attributes = True

class ParticipantVisitOut(BaseModel):
    id: str
    participant_id: str
    visit_name: Optional[str] = None
    scheduled_date: Optional[date] = None
    actual_date: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    class Config:
        from_attributes = True
