from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class AuditLogOut(BaseModel):
    id: str
    timestamp: Optional[datetime] = None
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    user_role: Optional[str] = None
    action: str
    entity_type: str
    entity_id: Optional[str] = None
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    ip_address: Optional[str] = None
    details: Optional[str] = None
    class Config:
        from_attributes = True
