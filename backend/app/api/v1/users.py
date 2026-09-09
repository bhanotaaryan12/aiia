from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.core.security import get_current_user, require_roles, get_password_hash
from app.models.user import User, Role, UserRole
from app.schemas.user import UserCreate, UserUpdate, UserOut, RoleOut
from typing import List

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserOut])
async def list_users(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN"))):
    result = await db.execute(select(User).where(User.is_deleted == False).offset(skip).limit(limit))
    users = result.scalars().all()
    out = []
    for u in users:
        roles_r = await db.execute(select(Role.name).join(UserRole, UserRole.role_id == Role.id).where(UserRole.user_id == u.id))
        role_names = [r[0] for r in roles_r.fetchall()]
        out.append(UserOut(id=u.id, email=u.email, username=u.username, full_name=u.full_name, is_active=u.is_active, is_superuser=u.is_superuser, created_at=u.created_at, roles=role_names))
    return out

@router.post("/", response_model=UserOut)
async def create_user(data: UserCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN"))):
    existing = await db.execute(select(User).where(User.email == data.email))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    user = User(email=data.email, username=data.username, full_name=data.full_name, hashed_password=get_password_hash(data.password), is_active=data.is_active)
    db.add(user)
    await db.flush()
    for rn in data.role_names:
        role_r = await db.execute(select(Role).where(Role.name == rn))
        role = role_r.scalar_one_or_none()
        if role:
            db.add(UserRole(user_id=user.id, role_id=role.id))
    await db.commit()
    return UserOut(id=user.id, email=user.email, username=user.username, full_name=user.full_name, is_active=user.is_active, is_superuser=user.is_superuser, roles=data.role_names)

@router.get("/roles", response_model=List[RoleOut])
async def list_roles(db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN"))):
    result = await db.execute(select(Role))
    return result.scalars().all()

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    user_roles = getattr(current_user, "role_names", [])
    is_admin = current_user.is_superuser or "SUPER_ADMIN" in user_roles or "TRIAL_ADMIN" in user_roles
    if current_user.id != user_id and not is_admin:
        raise HTTPException(status_code=403, detail="Insufficient permissions")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    roles_r = await db.execute(select(Role.name).join(UserRole, UserRole.role_id == Role.id).where(UserRole.user_id == user.id))
    role_names = [r[0] for r in roles_r.fetchall()]
    return UserOut(id=user.id, email=user.email, username=user.username, full_name=user.full_name, is_active=user.is_active, is_superuser=user.is_superuser, roles=role_names)
