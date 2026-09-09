import secrets

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, create_refresh_token, get_current_user, decode_token
from app.core.config import settings
from app.models.user import User, UserRole, Role
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])


def set_auth_cookies(response: Response, access_token: str, refresh_token: str) -> None:
    cookie_options = {"httponly": True, "secure": settings.COOKIE_SECURE, "samesite": "lax", "path": "/"}
    response.set_cookie("access_token", access_token, max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60, **cookie_options)
    response.set_cookie("refresh_token", refresh_token, max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400, **cookie_options)
    response.set_cookie("csrf_token", secrets.token_urlsafe(32), max_age=settings.REFRESH_TOKEN_EXPIRE_DAYS * 86400, httponly=False, secure=settings.COOKIE_SECURE, samesite="lax", path="/")

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, response: Response, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == request.email, User.is_active == True))
    user = result.scalar_one_or_none()
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    # Get user roles
    roles_result = await db.execute(
        select(Role.name).join(UserRole, UserRole.role_id == Role.id).where(UserRole.user_id == user.id)
    )
    role_names = [r[0] for r in roles_result.fetchall()]
    
    access_token = create_access_token(data={"sub": user.id, "email": user.email, "roles": role_names})
    refresh_token = create_refresh_token(data={"sub": user.id})
    
    user.last_login = datetime.now(timezone.utc)
    await db.commit()
    set_auth_cookies(response, access_token, refresh_token)
    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user = Depends(get_current_user)):
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        username=current_user.username,
        full_name=current_user.full_name,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        roles=getattr(current_user, "role_names", [])
    )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(refresh_token: str, response: Response, db: AsyncSession = Depends(get_db)):
    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=400, detail="Invalid refresh token")
    user_id = payload.get("sub")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    roles_result = await db.execute(
        select(Role.name).join(UserRole, UserRole.role_id == Role.id).where(UserRole.user_id == user.id)
    )
    role_names = [r[0] for r in roles_result.fetchall()]
    new_access = create_access_token(data={"sub": user.id, "email": user.email, "roles": role_names})
    new_refresh = create_refresh_token(data={"sub": user.id})
    set_auth_cookies(response, new_access, new_refresh)
    return TokenResponse(access_token=new_access, refresh_token=new_refresh)

@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    for name in ("access_token", "refresh_token", "csrf_token"):
        response.delete_cookie(name, path="/")
