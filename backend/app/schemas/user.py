from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    username: str
    full_name: str
    password: str
    is_active: bool = True
    role_names: List[str] = []

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role_names: Optional[List[str]] = None

class UserOut(BaseModel):
    id: str
    email: str
    username: str
    full_name: str
    is_active: bool
    is_superuser: bool
    created_at: Optional[datetime] = None
    roles: List[str] = []

    class Config:
        from_attributes = True

class RoleOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    class Config:
        from_attributes = True
