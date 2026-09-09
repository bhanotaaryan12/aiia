import os

BASE_DIR = r"c:\Users\nxahw\OneDrive\Desktop\proto\aiia-ctms\backend"

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# main.py
write_file("app/main.py", """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router
from app.core.database import engine, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
""")

# trials model
write_file("app/models/trial.py", """
from sqlalchemy import Column, String, Integer, Date, ForeignKey, Enum
from app.models.base import BaseModel
import enum

class TrialStatus(str, enum.Enum):
    PLANNING = "PLANNING"
    ETHICS_PENDING = "ETHICS_PENDING"
    ETHICS_APPROVED = "ETHICS_APPROVED"
    REGULATORY_PENDING = "REGULATORY_PENDING"
    REGISTERED = "REGISTERED"
    RECRUITING = "RECRUITING"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    SUSPENDED = "SUSPENDED"
    TERMINATED = "TERMINATED"

class Trial(BaseModel):
    __tablename__ = "trials"
    title = Column(String, nullable=False)
    short_title = Column(String, nullable=False)
    protocol_number = Column(String, unique=True, index=True)
    registration_number = Column(String, unique=True)
    phase = Column(String)
    status = Column(String, default=TrialStatus.PLANNING.value)
    sponsor = Column(String)
    pi_id = Column(String, ForeignKey("users.id"))
""")

# SECURITY
write_file("app/core/security.py", """
from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt
""")

# schemas
write_file("app/schemas/user.py", """
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: str
    is_active: bool = True
    is_superuser: bool = False

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
""")

write_file("app/schemas/trial.py", """
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from app.models.trial import TrialStatus

class TrialBase(BaseModel):
    title: str
    short_title: str
    protocol_number: str
    registration_number: Optional[str] = None
    phase: str
    status: TrialStatus = TrialStatus.PLANNING
    sponsor: str
    pi_id: Optional[str] = None

class TrialCreate(TrialBase):
    pass

class TrialResponse(TrialBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True
""")

# endpoints
write_file("app/api/v1/auth.py", """
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.models.user import User
from app.schemas.user import Token

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(db: AsyncSession = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    result = await db.execute(select(User).where(User.username == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}
""")

write_file("app/api/v1/users.py", """
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserCreate
from app.core.security import get_password_hash

router = APIRouter()

@router.get("/", response_model=List[UserResponse])
async def read_users(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()

@router.post("/", response_model=UserResponse)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    hashed_pwd = get_password_hash(user_in.password)
    new_user = User(
        email=user_in.email,
        username=user_in.username,
        full_name=user_in.full_name,
        hashed_password=hashed_pwd,
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
""")

write_file("app/api/v1/trials.py", """
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from app.core.database import get_db
from app.models.trial import Trial
from app.schemas.trial import TrialResponse, TrialCreate

router = APIRouter()

@router.get("/", response_model=List[TrialResponse])
async def read_trials(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Trial).offset(skip).limit(limit))
    return result.scalars().all()

@router.post("/", response_model=TrialResponse)
async def create_trial(trial_in: TrialCreate, db: AsyncSession = Depends(get_db)):
    new_trial = Trial(**trial_in.model_dump())
    db.add(new_trial)
    await db.commit()
    await db.refresh(new_trial)
    return new_trial
""")

write_file("app/api/v1/router.py", """
from fastapi import APIRouter
from app.api.v1 import auth, users, trials, sites, participants

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(trials.router, prefix="/trials", tags=["trials"])
""")
