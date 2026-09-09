import os

BASE_DIR = r"c:\Users\nxahw\OneDrive\Desktop\proto\aiia-ctms\backend"

def write_file(path, content):
    full_path = os.path.join(BASE_DIR, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")

# REQUIREMENTS & DOCKER
write_file("requirements.txt", """
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy[asyncio]==2.0.23
asyncpg==0.29.0
alembic==1.12.1
pydantic==2.5.2
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
python-dotenv==1.0.0
httpx==0.25.2
pytest==7.4.3
pytest-asyncio==0.21.1
aiofiles==23.2.1
""")

write_file("Dockerfile", """
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""")

write_file(".env.example", """
DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/aiia_ctms
SECRET_KEY=supersecretkey-for-ctms-aiia-gov
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
""")

# APP CORE
write_file("app/core/config.py", """
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List

class Settings(BaseSettings):
    PROJECT_NAME: str = "AIIA CTMS API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "supersecretkey-for-ctms-aiia-gov"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    DATABASE_URL: str = "sqlite+aiosqlite:///./sql_app.db" # Default for local dev, change to PG in prod
    
    CORS_ORIGINS: List[str] = ["*"]
    
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
""")

write_file("app/core/database.py", """
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings
import sys

# Handling connection strings for sqlite vs pg
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
else:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
""")

write_file("app/models/base.py", """
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base

def gen_uuid():
    return str(uuid.uuid4())

class BaseModel(Base):
    __abstract__ = True
    id = Column(UUID(as_uuid=False), primary_key=True, default=gen_uuid, index=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_deleted = Column(Boolean, default=False, index=True)
""")

write_file("app/models/user.py", """
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel

class User(BaseModel):
    __tablename__ = "users"
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    
    roles = relationship("UserRole", back_populates="user")

class Role(BaseModel):
    __tablename__ = "roles"
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String)
    is_system_role = Column(Boolean, default=True)

class UserRole(BaseModel):
    __tablename__ = "user_roles"
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    role_id = Column(String, ForeignKey("roles.id"), nullable=False)
    trial_id = Column(String, nullable=True) # Optional for trial-specific
    
    user = relationship("User", back_populates="roles")
    role = relationship("Role")
""")

write_file("app/models/trial.py", """
from sqlalchemy import Column, String, Integer, Date, ForeignKey, Enum
from .base import BaseModel
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

write_file("app/core/security.py", """
from datetime import datetime, timedelta, timezone
from typing import Any, Union
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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
from app.api.v1 import auth, users, trials

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(trials.router, prefix="/trials", tags=["trials"])
""")

write_file("app/main.py", """
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router
from app.core.database import engine, Base
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create tables on startup for this demo
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    # Clean up
    pass

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

print("Initial basic files generated successfully.")
