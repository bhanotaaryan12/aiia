from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentCreate(BaseModel):
    trial_id: Optional[str] = None
    title: str
    document_type: str = "OTHER"
    description: Optional[str] = None
    version: str = "1.0"

class DocumentOut(BaseModel):
    id: str
    trial_id: Optional[str] = None
    title: str
    document_type: str
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    version: str = "1.0"
    status: str = "ACTIVE"
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True
