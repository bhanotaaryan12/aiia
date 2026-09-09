from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    mfa_enabled = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
    phone = Column(String(20), nullable=True)
    department = Column(String(100), nullable=True)
    
    roles = relationship("UserRole", back_populates="user", lazy="selectin")

class Role(BaseModel):
    __tablename__ = "roles"
    name = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    is_system_role = Column(Boolean, default=True)
    
    permissions = relationship("RolePermission", back_populates="role", lazy="selectin")

class Permission(BaseModel):
    __tablename__ = "permissions"
    name = Column(String(100), unique=True, nullable=False)
    resource = Column(String(50), nullable=False)
    action = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)

class UserRole(BaseModel):
    __tablename__ = "user_roles"
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    role_id = Column(String(36), ForeignKey("roles.id"), nullable=False, index=True)
    trial_id = Column(String(36), ForeignKey("trials.id", use_alter=True), nullable=True)
    
    user = relationship("User", back_populates="roles")
    role = relationship("Role")

class RolePermission(BaseModel):
    __tablename__ = "role_permissions"
    role_id = Column(String(36), ForeignKey("roles.id"), nullable=False, index=True)
    permission_id = Column(String(36), ForeignKey("permissions.id"), nullable=False, index=True)
    
    role = relationship("Role", back_populates="permissions")
    permission = relationship("Permission")
