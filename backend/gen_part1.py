"""
AIIA CTMS Backend Generator - Part 1: Core Infrastructure & Models
Run this to generate the complete backend core files.
"""
import os

BASE = r"c:\Users\nxahw\OneDrive\Desktop\proto\aiia-ctms\backend"

def w(path, content):
    fp = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content.lstrip("\n"))

# ==============================================================
# requirements.txt
# ==============================================================
w("requirements.txt", """
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy[asyncio]==2.0.23
asyncpg==0.29.0
psycopg2-binary==2.9.9
alembic==1.12.1
pydantic==2.5.2
pydantic-settings==2.1.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6
python-dotenv==1.0.0
httpx==0.25.2
aiofiles==23.2.1
pytest==7.4.3
pytest-asyncio==0.21.1
email-validator==2.1.0
""")

# ==============================================================
# Dockerfile
# ==============================================================
w("Dockerfile", """
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/storage
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
""")

# ==============================================================
# app/__init__.py
# ==============================================================
w("app/__init__.py", "")

# ==============================================================
# app/core/__init__.py
# ==============================================================
w("app/core/__init__.py", "")

# ==============================================================
# app/core/config.py
# ==============================================================
w("app/core/config.py", '''
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List, Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "AIIA Clinical Trials Dashboard API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./aiia_ctms.db"
    DATABASE_URL_SYNC: str = "sqlite:///./aiia_ctms.db"

    # Security
    SECRET_KEY: str = "aiia-ctms-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Storage
    STORAGE_BACKEND: str = "local"
    STORAGE_LOCAL_PATH: str = "./storage"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
''')

# ==============================================================
# app/core/database.py
# ==============================================================
w("app/core/database.py", '''
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

if "sqlite" in settings.DATABASE_URL:
    engine = create_async_engine(settings.DATABASE_URL, echo=False)
else:
    engine = create_async_engine(settings.DATABASE_URL, echo=False, pool_size=20, max_overflow=10)

AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
''')

# ==============================================================
# app/core/security.py
# ==============================================================
w("app/core/security.py", '''
from datetime import datetime, timedelta, timezone
from typing import Optional, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.config import settings
from app.core.database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    from app.models.user import User, UserRole, Role
    payload = decode_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    result = await db.execute(select(User).where(User.id == user_id, User.is_active == True))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    # Load roles
    roles_result = await db.execute(
        select(Role.name).join(UserRole, UserRole.role_id == Role.id).where(UserRole.user_id == user_id)
    )
    user.role_names = [r[0] for r in roles_result.fetchall()]
    return user

def require_roles(*roles):
    async def role_checker(current_user = Depends(get_current_user)):
        if current_user.is_superuser:
            return current_user
        user_roles = getattr(current_user, "role_names", [])
        if "SUPER_ADMIN" in user_roles:
            return current_user
        if not any(r in user_roles for r in roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient permissions")
        return current_user
    return role_checker
''')

# ==============================================================
# app/models/__init__.py
# ==============================================================
w("app/models/__init__.py", '''
from app.models.base import BaseModel
from app.models.user import User, Role, Permission, UserRole, RolePermission
from app.models.trial import Trial, Protocol, StudyArm, Intervention, TrialMilestone
from app.models.site import Site, Investigator, SiteAssignment
from app.models.participant import Participant, Consent, Screening, Enrollment, Randomization, Withdrawal
from app.models.visit import VisitDefinition, ParticipantVisit
from app.models.form import Form, FormField, FormSubmission, DataPoint, DataQuery
from app.models.ethics import EthicsCommittee, EthicsSubmission, EthicsReview, EthicsApproval, ProtocolAmendment
from app.models.regulatory import RegulatoryRecord, RegulatoryChecklist
from app.models.pharmacovigilance import AdverseEvent, SeriousAdverseEvent, CausalityAssessment, SafetySignal
from app.models.document import Document
from app.models.audit import AuditLog
from app.models.notification import Notification
from app.models.cdisc import CDISCMapping
''')

# ==============================================================
# app/models/base.py
# ==============================================================
w("app/models/base.py", '''
import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Boolean
from app.core.database import Base

class BaseModel(Base):
    __abstract__ = True
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    is_deleted = Column(Boolean, default=False)
''')

# ==============================================================
# app/models/user.py
# ==============================================================
w("app/models/user.py", '''
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
''')

# ==============================================================
# app/models/trial.py
# ==============================================================
w("app/models/trial.py", '''
from sqlalchemy import Column, String, Integer, Date, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from .base import BaseModel

class Trial(BaseModel):
    __tablename__ = "trials"
    title = Column(String(500), nullable=False)
    short_title = Column(String(100), nullable=True)
    protocol_number = Column(String(50), unique=True, nullable=True, index=True)
    registration_number = Column(String(50), nullable=True)
    phase = Column(String(20), nullable=True)  # Phase 1, Phase 2, Phase 3, Phase 4
    study_type = Column(String(50), nullable=True)  # Interventional, Observational
    intervention_type = Column(String(50), nullable=True)
    therapeutic_area = Column(String(100), nullable=True)
    ayurveda_system = Column(String(100), nullable=True)
    primary_objective = Column(Text, nullable=True)
    secondary_objectives = Column(Text, nullable=True)
    inclusion_criteria = Column(Text, nullable=True)
    exclusion_criteria = Column(Text, nullable=True)
    planned_sample_size = Column(Integer, nullable=True)
    sponsor = Column(String(255), nullable=True)
    pi_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    start_date = Column(Date, nullable=True)
    expected_end_date = Column(Date, nullable=True)
    actual_end_date = Column(Date, nullable=True)
    status = Column(String(30), default="PLANNING", index=True)
    # PLANNING, ETHICS_PENDING, ETHICS_APPROVED, REGULATORY_PENDING, REGISTERED, RECRUITING, ACTIVE, COMPLETED, SUSPENDED, TERMINATED
    description = Column(Text, nullable=True)
    
    pi = relationship("User", foreign_keys=[pi_id])
    study_arms = relationship("StudyArm", back_populates="trial", lazy="selectin")
    interventions = relationship("Intervention", back_populates="trial", lazy="selectin")
    milestones = relationship("TrialMilestone", back_populates="trial", lazy="selectin")
    sites = relationship("SiteAssignment", back_populates="trial", lazy="selectin")

class Protocol(BaseModel):
    __tablename__ = "protocols"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    version = Column(String(20), nullable=False)
    title = Column(String(500), nullable=True)
    document_url = Column(String(500), nullable=True)
    effective_date = Column(Date, nullable=True)
    status = Column(String(20), default="DRAFT")  # DRAFT, ACTIVE, SUPERSEDED
    
    trial = relationship("Trial")

class StudyArm(BaseModel):
    __tablename__ = "study_arms"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    allocation_ratio = Column(Float, default=1.0)
    arm_type = Column(String(30), default="TREATMENT")  # TREATMENT, CONTROL, PLACEBO
    
    trial = relationship("Trial", back_populates="study_arms")

class Intervention(BaseModel):
    __tablename__ = "interventions"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    type = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    dosage = Column(String(200), nullable=True)
    duration = Column(String(100), nullable=True)
    formulation = Column(String(200), nullable=True)
    
    trial = relationship("Trial", back_populates="interventions")

class TrialMilestone(BaseModel):
    __tablename__ = "trial_milestones"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    planned_date = Column(Date, nullable=True)
    actual_date = Column(Date, nullable=True)
    status = Column(String(20), default="PENDING")  # PENDING, COMPLETED, DELAYED
    notes = Column(Text, nullable=True)
    
    trial = relationship("Trial", back_populates="milestones")
''')

# ==============================================================
# app/models/site.py
# ==============================================================
w("app/models/site.py", '''
from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class Site(BaseModel):
    __tablename__ = "sites"
    name = Column(String(255), nullable=False)
    institution = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    city = Column(String(100), nullable=True, index=True)
    state = Column(String(100), nullable=True)
    country = Column(String(100), default="India")
    pin_code = Column(String(10), nullable=True)
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    status = Column(String(20), default="ACTIVE")  # ACTIVE, INACTIVE, CLOSED
    activation_date = Column(Date, nullable=True)
    target_enrollment = Column(Integer, nullable=True)
    
    investigators = relationship("Investigator", back_populates="site", lazy="selectin")
    assignments = relationship("SiteAssignment", back_populates="site", lazy="selectin")

class Investigator(BaseModel):
    __tablename__ = "investigators"
    user_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    site_id = Column(String(36), ForeignKey("sites.id"), nullable=False, index=True)
    name = Column(String(255), nullable=False)
    qualification = Column(String(255), nullable=True)
    specialization = Column(String(255), nullable=True)
    experience_years = Column(Integer, nullable=True)
    gcp_trained = Column(Boolean, default=False)
    gcp_certificate_date = Column(Date, nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(20), nullable=True)
    
    site = relationship("Site", back_populates="investigators")
    user = relationship("User", foreign_keys=[user_id])

class SiteAssignment(BaseModel):
    __tablename__ = "site_assignments"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    site_id = Column(String(36), ForeignKey("sites.id"), nullable=False, index=True)
    pi_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    status = Column(String(20), default="PENDING")  # PENDING, ACTIVE, CLOSED
    activation_date = Column(Date, nullable=True)
    deactivation_date = Column(Date, nullable=True)
    target_enrollment = Column(Integer, nullable=True)
    
    trial = relationship("Trial", back_populates="sites")
    site = relationship("Site", back_populates="assignments")
    pi = relationship("User", foreign_keys=[pi_id])
''')

# ==============================================================
# app/models/participant.py
# ==============================================================
w("app/models/participant.py", '''
from sqlalchemy import Column, String, Date, Boolean, Text, ForeignKey, Integer
from sqlalchemy.orm import relationship
from .base import BaseModel

class Participant(BaseModel):
    __tablename__ = "participants"
    participant_id = Column(String(20), unique=True, nullable=False, index=True)  # Pseudonymous ID
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    site_id = Column(String(36), ForeignKey("sites.id"), nullable=False, index=True)
    screening_date = Column(Date, nullable=True)
    enrollment_date = Column(Date, nullable=True)
    status = Column(String(20), default="SCREENED", index=True)
    # SCREENED, ELIGIBLE, CONSENTED, ENROLLED, RANDOMIZED, ACTIVE, COMPLETED, WITHDRAWN
    age = Column(Integer, nullable=True)
    gender = Column(String(10), nullable=True)
    
    trial = relationship("Trial")
    site = relationship("Site")
    consents = relationship("Consent", back_populates="participant", lazy="selectin")
    visits = relationship("ParticipantVisit", back_populates="participant", lazy="selectin")
    adverse_events = relationship("AdverseEvent", back_populates="participant", lazy="selectin")

class Consent(BaseModel):
    __tablename__ = "consents"
    participant_id = Column(String(36), ForeignKey("participants.id"), nullable=False, index=True)
    consent_type = Column(String(50), default="INFORMED_CONSENT")
    consent_date = Column(Date, nullable=False)
    consent_version = Column(String(20), nullable=True)
    consented_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    witness_name = Column(String(255), nullable=True)
    withdrawn = Column(Boolean, default=False)
    withdrawal_date = Column(Date, nullable=True)
    withdrawal_reason = Column(Text, nullable=True)
    
    participant = relationship("Participant", back_populates="consents")

class Screening(BaseModel):
    __tablename__ = "screenings"
    participant_id = Column(String(36), ForeignKey("participants.id"), nullable=False, index=True)
    screening_date = Column(Date, nullable=False)
    eligible = Column(Boolean, nullable=True)
    ineligibility_reason = Column(Text, nullable=True)
    screened_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)
    
    participant = relationship("Participant")

class Enrollment(BaseModel):
    __tablename__ = "enrollments"
    participant_id = Column(String(36), ForeignKey("participants.id"), nullable=False, unique=True)
    enrollment_date = Column(Date, nullable=False)
    enrolled_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    enrollment_number = Column(String(20), nullable=True)
    
    participant = relationship("Participant")

class Randomization(BaseModel):
    __tablename__ = "randomizations"
    participant_id = Column(String(36), ForeignKey("participants.id"), nullable=False, unique=True)
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False)
    randomization_date = Column(Date, nullable=False)
    randomization_number = Column(String(20), nullable=True)
    assigned_arm_id = Column(String(36), ForeignKey("study_arms.id"), nullable=True)
    assigned_arm_name = Column(String(100), nullable=True)
    randomized_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    is_locked = Column(Boolean, default=True)
    
    participant = relationship("Participant")
    arm = relationship("StudyArm")

class Withdrawal(BaseModel):
    __tablename__ = "withdrawals"
    participant_id = Column(String(36), ForeignKey("participants.id"), nullable=False, index=True)
    withdrawal_date = Column(Date, nullable=False)
    reason = Column(Text, nullable=True)
    withdrawn_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)
    
    participant = relationship("Participant")
''')

# ==============================================================
# app/models/visit.py
# ==============================================================
w("app/models/visit.py", '''
from sqlalchemy import Column, String, Integer, Date, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class VisitDefinition(BaseModel):
    __tablename__ = "visit_definitions"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    visit_name = Column(String(100), nullable=False)
    visit_number = Column(Integer, nullable=False)
    visit_type = Column(String(30), default="TREATMENT")
    # SCREENING, BASELINE, TREATMENT, FOLLOW_UP, END_OF_STUDY
    day_offset = Column(Integer, default=0)
    window_before = Column(Integer, default=3)
    window_after = Column(Integer, default=3)
    is_required = Column(Boolean, default=True)
    
    trial = relationship("Trial")

class ParticipantVisit(BaseModel):
    __tablename__ = "participant_visits"
    participant_id = Column(String(36), ForeignKey("participants.id"), nullable=False, index=True)
    visit_definition_id = Column(String(36), ForeignKey("visit_definitions.id"), nullable=True)
    visit_name = Column(String(100), nullable=True)
    scheduled_date = Column(Date, nullable=True)
    actual_date = Column(Date, nullable=True)
    status = Column(String(20), default="SCHEDULED", index=True)
    # SCHEDULED, COMPLETED, MISSED, OVERDUE, CANCELLED
    notes = Column(Text, nullable=True)
    completed_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    
    participant = relationship("Participant", back_populates="visits")
    visit_definition = relationship("VisitDefinition")
''')

# ==============================================================
# app/models/form.py
# ==============================================================
w("app/models/form.py", '''
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Text, DateTime, JSON
from sqlalchemy.orm import relationship
from .base import BaseModel

class Form(BaseModel):
    __tablename__ = "forms"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), nullable=True)
    description = Column(Text, nullable=True)
    version = Column(String(20), default="1.0")
    status = Column(String(20), default="ACTIVE")  # DRAFT, ACTIVE, RETIRED
    visit_type = Column(String(30), nullable=True)
    
    trial = relationship("Trial")
    fields = relationship("FormField", back_populates="form", lazy="selectin", order_by="FormField.order_index")

class FormField(BaseModel):
    __tablename__ = "form_fields"
    form_id = Column(String(36), ForeignKey("forms.id"), nullable=False, index=True)
    field_name = Column(String(100), nullable=False)
    field_label = Column(String(255), nullable=False)
    field_type = Column(String(30), nullable=False)
    # TEXT, NUMBER, DATE, DATETIME, BOOLEAN, SINGLE_SELECT, MULTI_SELECT, LAB_VALUE
    is_required = Column(Boolean, default=False)
    validation_rules = Column(JSON, nullable=True)  # {"min": 0, "max": 200}
    options = Column(JSON, nullable=True)  # ["option1", "option2"]
    order_index = Column(Integer, default=0)
    cdisc_domain = Column(String(10), nullable=True)
    cdisc_variable = Column(String(20), nullable=True)
    unit = Column(String(30), nullable=True)
    
    form = relationship("Form", back_populates="fields")

class FormSubmission(BaseModel):
    __tablename__ = "form_submissions"
    form_id = Column(String(36), ForeignKey("forms.id"), nullable=False, index=True)
    participant_id = Column(String(36), ForeignKey("participants.id"), nullable=False, index=True)
    visit_id = Column(String(36), ForeignKey("participant_visits.id"), nullable=True)
    submitted_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    submitted_at = Column(DateTime, nullable=True)
    status = Column(String(20), default="DRAFT")  # DRAFT, SUBMITTED, VERIFIED, LOCKED
    data = Column(JSON, nullable=True)
    
    form = relationship("Form")
    participant = relationship("Participant")

class DataPoint(BaseModel):
    __tablename__ = "data_points"
    submission_id = Column(String(36), ForeignKey("form_submissions.id"), nullable=False, index=True)
    field_id = Column(String(36), ForeignKey("form_fields.id"), nullable=False)
    value = Column(Text, nullable=True)
    is_valid = Column(Boolean, default=True)
    validation_message = Column(Text, nullable=True)
    
    submission = relationship("FormSubmission")
    field = relationship("FormField")

class DataQuery(BaseModel):
    __tablename__ = "data_queries"
    submission_id = Column(String(36), ForeignKey("form_submissions.id"), nullable=False, index=True)
    field_id = Column(String(36), ForeignKey("form_fields.id"), nullable=True)
    query_text = Column(Text, nullable=False)
    query_type = Column(String(30), default="MANUAL")  # MANUAL, AUTO_VALIDATION
    status = Column(String(20), default="OPEN", index=True)  # OPEN, ANSWERED, RESOLVED, CLOSED
    raised_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    answered_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    answer_text = Column(Text, nullable=True)
    resolved_at = Column(DateTime, nullable=True)
    
    submission = relationship("FormSubmission")
''')

# ==============================================================
# app/models/ethics.py
# ==============================================================
w("app/models/ethics.py", '''
from sqlalchemy import Column, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class EthicsCommittee(BaseModel):
    __tablename__ = "ethics_committees"
    name = Column(String(255), nullable=False)
    institution = Column(String(255), nullable=True)
    address = Column(Text, nullable=True)
    registration_number = Column(String(50), nullable=True)
    chairperson = Column(String(255), nullable=True)
    contact_email = Column(String(255), nullable=True)

class EthicsSubmission(BaseModel):
    __tablename__ = "ethics_submissions"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    committee_id = Column(String(36), ForeignKey("ethics_committees.id"), nullable=True)
    submission_type = Column(String(30), default="INITIAL")
    # INITIAL, AMENDMENT, RENEWAL, SAE_REPORT
    submission_date = Column(Date, nullable=True)
    status = Column(String(30), default="DRAFT", index=True)
    # DRAFT, SUBMITTED, UNDER_REVIEW, CLARIFICATION_REQUIRED, APPROVED, REJECTED
    submitted_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    title = Column(String(500), nullable=True)
    description = Column(Text, nullable=True)
    
    trial = relationship("Trial")
    committee = relationship("EthicsCommittee")
    reviews = relationship("EthicsReview", back_populates="submission", lazy="selectin")
    approval = relationship("EthicsApproval", back_populates="submission", uselist=False, lazy="selectin")

class EthicsReview(BaseModel):
    __tablename__ = "ethics_reviews"
    submission_id = Column(String(36), ForeignKey("ethics_submissions.id"), nullable=False, index=True)
    reviewer = Column(String(255), nullable=True)
    review_date = Column(Date, nullable=True)
    decision = Column(String(30), nullable=True)  # APPROVED, REJECTED, REVISIONS_REQUIRED
    comments = Column(Text, nullable=True)
    conditions = Column(Text, nullable=True)
    
    submission = relationship("EthicsSubmission", back_populates="reviews")

class EthicsApproval(BaseModel):
    __tablename__ = "ethics_approvals"
    submission_id = Column(String(36), ForeignKey("ethics_submissions.id"), nullable=False)
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False)
    approval_number = Column(String(50), nullable=True)
    approval_date = Column(Date, nullable=True)
    valid_from = Column(Date, nullable=True)
    valid_until = Column(Date, nullable=True)
    conditions = Column(Text, nullable=True)
    document_url = Column(String(500), nullable=True)
    
    submission = relationship("EthicsSubmission", back_populates="approval")
    trial = relationship("Trial")

class ProtocolAmendment(BaseModel):
    __tablename__ = "protocol_amendments"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    amendment_number = Column(String(20), nullable=False)
    description = Column(Text, nullable=True)
    submission_date = Column(Date, nullable=True)
    approval_date = Column(Date, nullable=True)
    status = Column(String(20), default="DRAFT")  # DRAFT, SUBMITTED, APPROVED, REJECTED
    changes_summary = Column(Text, nullable=True)
    
    trial = relationship("Trial")
''')

# ==============================================================
# app/models/regulatory.py
# ==============================================================
w("app/models/regulatory.py", '''
from sqlalchemy import Column, String, Date, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class RegulatoryRecord(BaseModel):
    __tablename__ = "regulatory_records"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    record_type = Column(String(20), default="CTRI")  # CTRI, DCGI, IEC, OTHER
    registration_number = Column(String(50), nullable=True)
    submission_date = Column(Date, nullable=True)
    registration_date = Column(Date, nullable=True)
    status = Column(String(30), default="NOT_STARTED", index=True)
    # NOT_STARTED, PREPARING, SUBMITTED, UNDER_REVIEW, REGISTERED, UPDATE_REQUIRED, COMPLETED
    last_verified_date = Column(Date, nullable=True)
    responsible_officer_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    notes = Column(Text, nullable=True)
    
    trial = relationship("Trial")
    officer = relationship("User", foreign_keys=[responsible_officer_id])

class RegulatoryChecklist(BaseModel):
    __tablename__ = "regulatory_checklists"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    category = Column(String(30), default="NDCT_RULES_2019")  # NDCT_RULES_2019, GCP, ICH
    item_name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_completed = Column(Boolean, default=False)
    completed_date = Column(Date, nullable=True)
    completed_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    evidence_document_id = Column(String(36), ForeignKey("documents.id", use_alter=True), nullable=True)
    notes = Column(Text, nullable=True)
    
    trial = relationship("Trial")
''')

# ==============================================================
# app/models/pharmacovigilance.py
# ==============================================================
w("app/models/pharmacovigilance.py", '''
from sqlalchemy import Column, String, Date, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class AdverseEvent(BaseModel):
    __tablename__ = "adverse_events"
    participant_id = Column(String(36), ForeignKey("participants.id"), nullable=False, index=True)
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    site_id = Column(String(36), ForeignKey("sites.id"), nullable=True)
    event_term = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    onset_date = Column(Date, nullable=True)
    resolution_date = Column(Date, nullable=True)
    severity = Column(String(20), default="MILD")  # MILD, MODERATE, SEVERE
    seriousness = Column(String(20), default="NON_SERIOUS")  # NON_SERIOUS, SERIOUS
    causality = Column(String(20), default="POSSIBLE")
    # UNRELATED, UNLIKELY, POSSIBLE, PROBABLE, DEFINITE
    expectedness = Column(String(20), default="EXPECTED")  # EXPECTED, UNEXPECTED
    action_taken = Column(Text, nullable=True)
    outcome = Column(String(30), default="UNKNOWN")
    # RECOVERED, RECOVERING, NOT_RECOVERED, FATAL, UNKNOWN
    reporter_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    reported_date = Column(Date, nullable=True)
    status = Column(String(20), default="REPORTED", index=True)
    
    participant = relationship("Participant", back_populates="adverse_events")
    trial = relationship("Trial")
    site = relationship("Site")

class SeriousAdverseEvent(BaseModel):
    __tablename__ = "serious_adverse_events"
    adverse_event_id = Column(String(36), ForeignKey("adverse_events.id"), nullable=False, index=True)
    sae_number = Column(String(20), nullable=True, unique=True)
    criteria = Column(String(30), nullable=True)
    # DEATH, LIFE_THREATENING, HOSPITALIZATION, DISABILITY, CONGENITAL_ANOMALY, OTHER
    narrative = Column(Text, nullable=True)
    reported_to_sponsor_date = Column(Date, nullable=True)
    reported_to_ethics_date = Column(Date, nullable=True)
    reported_to_regulatory_date = Column(Date, nullable=True)
    status = Column(String(30), default="REPORTED", index=True)
    # REPORTED, UNDER_REVIEW, MEDICAL_REVIEW, REGULATORY_REVIEW, SUBMITTED, CLOSED
    
    adverse_event = relationship("AdverseEvent")

class CausalityAssessment(BaseModel):
    __tablename__ = "causality_assessments"
    adverse_event_id = Column(String(36), ForeignKey("adverse_events.id"), nullable=False, index=True)
    assessor_id = Column(String(36), ForeignKey("users.id"), nullable=True)
    assessment_date = Column(Date, nullable=True)
    method = Column(String(50), nullable=True)  # WHO-UMC, Naranjo
    causality_rating = Column(String(20), nullable=True)
    rationale = Column(Text, nullable=True)
    
    adverse_event = relationship("AdverseEvent")

class SafetySignal(BaseModel):
    __tablename__ = "safety_signals"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=False, index=True)
    signal_term = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    detected_date = Column(Date, nullable=True)
    status = Column(String(20), default="DETECTED")  # DETECTED, UNDER_REVIEW, CONFIRMED, CLOSED
    severity = Column(String(20), nullable=True)
    action_taken = Column(Text, nullable=True)
    
    trial = relationship("Trial")
''')

# ==============================================================
# app/models/document.py
# ==============================================================
w("app/models/document.py", '''
from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from .base import BaseModel

class Document(BaseModel):
    __tablename__ = "documents"
    trial_id = Column(String(36), ForeignKey("trials.id"), nullable=True, index=True)
    title = Column(String(255), nullable=False)
    document_type = Column(String(30), default="OTHER")
    # PROTOCOL, CONSENT_FORM, ETHICS_APPROVAL, REGULATORY, INVESTIGATOR_BROCHURE, SAFETY_REPORT, OTHER
    file_name = Column(String(255), nullable=True)
    file_path = Column(String(500), nullable=True)
    file_size = Column(Integer, nullable=True)
    mime_type = Column(String(100), nullable=True)
    uploaded_by = Column(String(36), ForeignKey("users.id"), nullable=True)
    version = Column(String(20), default="1.0")
    status = Column(String(20), default="ACTIVE")  # ACTIVE, ARCHIVED
    description = Column(Text, nullable=True)
    
    trial = relationship("Trial")
''')

# ==============================================================
# app/models/audit.py
# ==============================================================
w("app/models/audit.py", '''
from sqlalchemy import Column, String, DateTime, Text, JSON
from app.core.database import Base
import uuid
from datetime import datetime, timezone

class AuditLog(Base):
    """Append-only audit log - no updates or deletes."""
    __tablename__ = "audit_logs"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    user_id = Column(String(36), nullable=True, index=True)
    user_email = Column(String(255), nullable=True)
    user_role = Column(String(50), nullable=True)
    action = Column(String(50), nullable=False, index=True)
    entity_type = Column(String(50), nullable=False, index=True)
    entity_id = Column(String(36), nullable=True)
    old_value = Column(JSON, nullable=True)
    new_value = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    user_agent = Column(String(500), nullable=True)
    reason = Column(Text, nullable=True)
    details = Column(Text, nullable=True)
''')

# ==============================================================
# app/models/notification.py
# ==============================================================
w("app/models/notification.py", '''
from sqlalchemy import Column, String, Boolean, DateTime, Text, ForeignKey
from .base import BaseModel

class Notification(BaseModel):
    __tablename__ = "notifications"
    user_id = Column(String(36), ForeignKey("users.id"), nullable=False, index=True)
    title = Column(String(255), nullable=False)
    message = Column(Text, nullable=True)
    type = Column(String(30), default="SYSTEM")
    # SAE_REPORTED, ETHICS_EXPIRING, REGULATORY_DEADLINE, OVERDUE_VISIT, DATA_QUERY, PROTOCOL_DEVIATION, SYSTEM
    entity_type = Column(String(50), nullable=True)
    entity_id = Column(String(36), nullable=True)
    is_read = Column(Boolean, default=False, index=True)
    read_at = Column(DateTime, nullable=True)
    priority = Column(String(10), default="NORMAL")  # LOW, NORMAL, HIGH, URGENT
''')

# ==============================================================
# app/models/cdisc.py
# ==============================================================
w("app/models/cdisc.py", '''
from sqlalchemy import Column, String, Boolean, Text
from .base import BaseModel

class CDISCMapping(BaseModel):
    __tablename__ = "cdisc_mappings"
    internal_entity = Column(String(100), nullable=False)
    internal_field = Column(String(100), nullable=False)
    cdisc_domain = Column(String(10), nullable=False)
    cdisc_variable = Column(String(30), nullable=False)
    transformation_rule = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
''')

print("Part 1 (Core + Models) generated successfully.")
