from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationOut(BaseModel):
    id: str
    user_id: str
    title: str
    message: Optional[str] = None
    type: str
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    is_read: bool = False
    read_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    priority: str = "NORMAL"
    class Config:
        from_attributes = True
