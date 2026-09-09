from pydantic import BaseModel
from typing import Optional, Any, List, Dict
from datetime import datetime

class FormCreate(BaseModel):
    trial_id: str
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    visit_type: Optional[str] = None

class FormFieldCreate(BaseModel):
    form_id: str
    field_name: str
    field_label: str
    field_type: str = "TEXT"
    is_required: bool = False
    validation_rules: Optional[Dict] = None
    options: Optional[List[str]] = None
    order_index: int = 0
    unit: Optional[str] = None
    cdisc_domain: Optional[str] = None
    cdisc_variable: Optional[str] = None

class FormSubmissionCreate(BaseModel):
    form_id: str
    participant_id: str
    visit_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    status: str = "DRAFT"

class FormSubmissionUpdate(BaseModel):
    data: Optional[Dict[str, Any]] = None
    status: Optional[str] = None

class DataQueryCreate(BaseModel):
    submission_id: str
    field_id: Optional[str] = None
    query_text: str
    query_type: str = "MANUAL"

class DataQueryUpdate(BaseModel):
    answer_text: Optional[str] = None
    status: Optional[str] = None

class FormOut(BaseModel):
    id: str
    trial_id: str
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    version: Optional[str] = None
    class Config:
        from_attributes = True

class FormFieldOut(BaseModel):
    id: str
    form_id: str
    field_name: str
    field_label: str
    field_type: str
    is_required: bool = False
    validation_rules: Optional[Dict] = None
    options: Optional[List[str]] = None
    order_index: int = 0
    unit: Optional[str] = None
    class Config:
        from_attributes = True

class FormSubmissionOut(BaseModel):
    id: str
    form_id: str
    participant_id: str
    submitted_at: Optional[datetime] = None
    status: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    class Config:
        from_attributes = True

class DataQueryOut(BaseModel):
    id: str
    submission_id: str
    query_text: str
    query_type: str
    status: str
    answer_text: Optional[str] = None
    class Config:
        from_attributes = True
