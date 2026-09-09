"""
AIIA CTMS Backend Generator - Part 3: API Routes + Main App + Seed Data
"""
import os

BASE = r"c:\Users\nxahw\OneDrive\Desktop\proto\aiia-ctms\backend"

def w(path, content):
    fp = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content.lstrip("\n"))

# ==============================================================
# API ROUTES
# ==============================================================
w("app/api/__init__.py", "")
w("app/api/v1/__init__.py", "")

w("app/api/v1/auth.py", '''
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from app.core.database import get_db
from app.core.security import verify_password, create_access_token, create_refresh_token, get_current_user, decode_token
from app.models.user import User, UserRole, Role
from app.schemas.auth import LoginRequest, TokenResponse, UserResponse

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
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
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
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
    return TokenResponse(access_token=new_access, refresh_token=new_refresh)
''')

w("app/api/v1/users.py", '''
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
async def list_roles(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Role))
    return result.scalars().all()

@router.get("/{user_id}", response_model=UserOut)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    roles_r = await db.execute(select(Role.name).join(UserRole, UserRole.role_id == Role.id).where(UserRole.user_id == user.id))
    role_names = [r[0] for r in roles_r.fetchall()]
    return UserOut(id=user.id, email=user.email, username=user.username, full_name=user.full_name, is_active=user.is_active, is_superuser=user.is_superuser, roles=role_names)
''')

w("app/api/v1/trials.py", '''
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.trial import Trial, StudyArm, Intervention, TrialMilestone
from app.models.participant import Participant
from app.models.site import SiteAssignment
from app.schemas.trial import TrialCreate, TrialUpdate, TrialOut, StudyArmCreate, InterventionCreate, MilestoneCreate, StudyArmOut
from typing import List, Optional

router = APIRouter(prefix="/trials", tags=["Trials"])

@router.get("/", response_model=List[TrialOut])
async def list_trials(skip: int = 0, limit: int = 50, status: Optional[str] = None, phase: Optional[str] = None, search: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(Trial).where(Trial.is_deleted == False)
    if status:
        query = query.where(Trial.status == status)
    if phase:
        query = query.where(Trial.phase == phase)
    if search:
        query = query.where(Trial.title.ilike(f"%{search}%"))
    query = query.order_by(Trial.created_at.desc()).offset(skip).limit(limit)
    result = await db.execute(query)
    trials = result.scalars().all()
    out = []
    for t in trials:
        pc = await db.execute(select(func.count()).select_from(Participant).where(Participant.trial_id == t.id, Participant.is_deleted == False))
        sc = await db.execute(select(func.count()).select_from(SiteAssignment).where(SiteAssignment.trial_id == t.id))
        out.append(TrialOut(
            id=t.id, title=t.title, short_title=t.short_title, protocol_number=t.protocol_number,
            registration_number=t.registration_number, phase=t.phase, study_type=t.study_type,
            intervention_type=t.intervention_type, therapeutic_area=t.therapeutic_area,
            ayurveda_system=t.ayurveda_system, primary_objective=t.primary_objective,
            planned_sample_size=t.planned_sample_size, sponsor=t.sponsor,
            start_date=t.start_date, expected_end_date=t.expected_end_date,
            actual_end_date=t.actual_end_date, status=t.status, description=t.description,
            created_at=t.created_at, participant_count=pc.scalar() or 0, site_count=sc.scalar() or 0
        ))
    return out

@router.post("/", response_model=TrialOut)
async def create_trial(data: TrialCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN", "PRINCIPAL_INVESTIGATOR"))):
    trial = Trial(**data.model_dump())
    db.add(trial)
    await db.commit()
    await db.refresh(trial)
    return TrialOut(id=trial.id, title=trial.title, short_title=trial.short_title, protocol_number=trial.protocol_number, phase=trial.phase, status=trial.status, created_at=trial.created_at, study_type=trial.study_type, therapeutic_area=trial.therapeutic_area, start_date=trial.start_date, expected_end_date=trial.expected_end_date, planned_sample_size=trial.planned_sample_size, sponsor=trial.sponsor, description=trial.description)

@router.get("/{trial_id}", response_model=TrialOut)
async def get_trial(trial_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Trial).where(Trial.id == trial_id))
    trial = result.scalar_one_or_none()
    if not trial:
        raise HTTPException(status_code=404, detail="Trial not found")
    pc = await db.execute(select(func.count()).select_from(Participant).where(Participant.trial_id == trial.id))
    sc = await db.execute(select(func.count()).select_from(SiteAssignment).where(SiteAssignment.trial_id == trial.id))
    return TrialOut(
        id=trial.id, title=trial.title, short_title=trial.short_title, protocol_number=trial.protocol_number,
        registration_number=trial.registration_number, phase=trial.phase, study_type=trial.study_type,
        intervention_type=trial.intervention_type, therapeutic_area=trial.therapeutic_area,
        ayurveda_system=trial.ayurveda_system, primary_objective=trial.primary_objective,
        planned_sample_size=trial.planned_sample_size, sponsor=trial.sponsor,
        start_date=trial.start_date, expected_end_date=trial.expected_end_date, status=trial.status,
        description=trial.description, created_at=trial.created_at, participant_count=pc.scalar() or 0, site_count=sc.scalar() or 0
    )

@router.put("/{trial_id}", response_model=TrialOut)
async def update_trial(trial_id: str, data: TrialUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN", "PRINCIPAL_INVESTIGATOR"))):
    result = await db.execute(select(Trial).where(Trial.id == trial_id))
    trial = result.scalar_one_or_none()
    if not trial:
        raise HTTPException(status_code=404, detail="Trial not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(trial, key, value)
    await db.commit()
    return TrialOut(id=trial.id, title=trial.title, short_title=trial.short_title, protocol_number=trial.protocol_number, phase=trial.phase, status=trial.status, created_at=trial.created_at)

@router.get("/{trial_id}/arms", response_model=List[StudyArmOut])
async def get_trial_arms(trial_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(StudyArm).where(StudyArm.trial_id == trial_id))
    return result.scalars().all()

@router.post("/{trial_id}/arms", response_model=StudyArmOut)
async def create_study_arm(trial_id: str, data: StudyArmCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN"))):
    arm = StudyArm(trial_id=trial_id, **data.model_dump())
    db.add(arm)
    await db.commit()
    await db.refresh(arm)
    return arm
''')

w("app/api/v1/sites.py", '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.site import Site, Investigator, SiteAssignment
from app.models.participant import Participant
from app.schemas.site import SiteCreate, SiteUpdate, SiteOut, InvestigatorCreate, InvestigatorOut, SiteAssignmentCreate
from typing import List, Optional

router = APIRouter(prefix="/sites", tags=["Sites"])

@router.get("/", response_model=List[SiteOut])
async def list_sites(skip: int = 0, limit: int = 50, status: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(Site).where(Site.is_deleted == False)
    if status:
        query = query.where(Site.status == status)
    result = await db.execute(query.offset(skip).limit(limit))
    sites = result.scalars().all()
    out = []
    for s in sites:
        pc = await db.execute(select(func.count()).select_from(Participant).where(Participant.site_id == s.id, Participant.is_deleted == False))
        out.append(SiteOut(id=s.id, name=s.name, institution=s.institution, city=s.city, state=s.state, status=s.status, target_enrollment=s.target_enrollment, activation_date=s.activation_date, created_at=s.created_at, participant_count=pc.scalar() or 0))
    return out

@router.post("/", response_model=SiteOut)
async def create_site(data: SiteCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN"))):
    site = Site(**data.model_dump())
    db.add(site)
    await db.commit()
    await db.refresh(site)
    return SiteOut(id=site.id, name=site.name, institution=site.institution, city=site.city, state=site.state, status=site.status, target_enrollment=site.target_enrollment, created_at=site.created_at)

@router.get("/{site_id}", response_model=SiteOut)
async def get_site(site_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Site).where(Site.id == site_id))
    site = result.scalar_one_or_none()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    pc = await db.execute(select(func.count()).select_from(Participant).where(Participant.site_id == site.id))
    return SiteOut(id=site.id, name=site.name, institution=site.institution, city=site.city, state=site.state, status=site.status, target_enrollment=site.target_enrollment, created_at=site.created_at, participant_count=pc.scalar() or 0)

@router.put("/{site_id}", response_model=SiteOut)
async def update_site(site_id: str, data: SiteUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN"))):
    result = await db.execute(select(Site).where(Site.id == site_id))
    site = result.scalar_one_or_none()
    if not site:
        raise HTTPException(status_code=404, detail="Site not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(site, key, value)
    await db.commit()
    return SiteOut(id=site.id, name=site.name, institution=site.institution, city=site.city, state=site.state, status=site.status, target_enrollment=site.target_enrollment)

@router.post("/assignments")
async def create_site_assignment(data: SiteAssignmentCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN"))):
    sa = SiteAssignment(**data.model_dump(), status="ACTIVE")
    db.add(sa)
    await db.commit()
    return {"id": sa.id, "status": "created"}

@router.get("/investigators/all", response_model=List[InvestigatorOut])
async def list_investigators(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Investigator).where(Investigator.is_deleted == False))
    return result.scalars().all()

@router.post("/investigators", response_model=InvestigatorOut)
async def create_investigator(data: InvestigatorCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN"))):
    inv = Investigator(**data.model_dump())
    db.add(inv)
    await db.commit()
    await db.refresh(inv)
    return inv
''')

w("app/api/v1/participants.py", '''
import random, string
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.participant import Participant, Consent, Screening, Enrollment, Randomization
from app.models.trial import StudyArm
from app.schemas.participant import ParticipantCreate, ParticipantUpdate, ParticipantOut, ConsentCreate, ScreeningCreate, EnrollmentCreate, RandomizationOut
from typing import List, Optional

router = APIRouter(prefix="/participants", tags=["Participants"])

def generate_participant_id():
    return "AIIA-" + "".join(random.choices(string.digits, k=6))

@router.get("/", response_model=List[ParticipantOut])
async def list_participants(skip: int = 0, limit: int = 100, trial_id: Optional[str] = None, site_id: Optional[str] = None, status: Optional[str] = None, search: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(Participant).where(Participant.is_deleted == False)
    if trial_id:
        query = query.where(Participant.trial_id == trial_id)
    if site_id:
        query = query.where(Participant.site_id == site_id)
    if status:
        query = query.where(Participant.status == status)
    if search:
        query = query.where(Participant.participant_id.ilike(f"%{search}%"))
    result = await db.execute(query.order_by(Participant.created_at.desc()).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/count")
async def count_participants(trial_id: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(func.count()).select_from(Participant).where(Participant.is_deleted == False)
    if trial_id:
        query = query.where(Participant.trial_id == trial_id)
    result = await db.execute(query)
    return {"count": result.scalar() or 0}

@router.post("/", response_model=ParticipantOut)
async def create_participant(data: ParticipantCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN", "PRINCIPAL_INVESTIGATOR", "STUDY_COORDINATOR"))):
    p = Participant(participant_id=generate_participant_id(), trial_id=data.trial_id, site_id=data.site_id, screening_date=date.today(), status="SCREENED", age=data.age, gender=data.gender)
    db.add(p)
    await db.commit()
    await db.refresh(p)
    return p

@router.get("/{participant_id}", response_model=ParticipantOut)
async def get_participant(participant_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Participant).where(Participant.id == participant_id))
    p = result.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail="Participant not found")
    return p

@router.put("/{participant_id}", response_model=ParticipantOut)
async def update_participant(participant_id: str, data: ParticipantUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "PRINCIPAL_INVESTIGATOR", "STUDY_COORDINATOR"))):
    result = await db.execute(select(Participant).where(Participant.id == participant_id))
    p = result.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail="Participant not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(p, key, value)
    await db.commit()
    return p

@router.post("/{participant_id}/consent")
async def record_consent(participant_id: str, data: ConsentCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "PRINCIPAL_INVESTIGATOR", "STUDY_COORDINATOR"))):
    consent = Consent(participant_id=participant_id, consent_date=data.consent_date, consent_version=data.consent_version, witness_name=data.witness_name, consented_by=current_user.id)
    db.add(consent)
    result = await db.execute(select(Participant).where(Participant.id == participant_id))
    p = result.scalar_one_or_none()
    if p:
        p.status = "CONSENTED"
    await db.commit()
    return {"status": "consent_recorded", "id": consent.id}

@router.post("/{participant_id}/enroll")
async def enroll_participant(participant_id: str, data: EnrollmentCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "PRINCIPAL_INVESTIGATOR", "STUDY_COORDINATOR"))):
    enrollment = Enrollment(participant_id=participant_id, enrollment_date=data.enrollment_date, enrolled_by=current_user.id)
    db.add(enrollment)
    result = await db.execute(select(Participant).where(Participant.id == participant_id))
    p = result.scalar_one_or_none()
    if p:
        p.status = "ENROLLED"
        p.enrollment_date = data.enrollment_date
    await db.commit()
    return {"status": "enrolled", "id": enrollment.id}

@router.post("/{participant_id}/randomize", response_model=RandomizationOut)
async def randomize_participant(participant_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "PRINCIPAL_INVESTIGATOR", "STUDY_COORDINATOR"))):
    result = await db.execute(select(Participant).where(Participant.id == participant_id))
    p = result.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail="Participant not found")
    # Check not already randomized
    existing = await db.execute(select(Randomization).where(Randomization.participant_id == participant_id))
    if existing.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Already randomized")
    # Get trial arms
    arms_r = await db.execute(select(StudyArm).where(StudyArm.trial_id == p.trial_id))
    arms = arms_r.scalars().all()
    if not arms:
        raise HTTPException(status_code=400, detail="No study arms defined")
    # Simple weighted randomization
    weights = [a.allocation_ratio for a in arms]
    selected = random.choices(arms, weights=weights, k=1)[0]
    rand_num = "R-" + "".join(random.choices(string.digits, k=6))
    randomization = Randomization(participant_id=participant_id, trial_id=p.trial_id, randomization_date=date.today(), randomization_number=rand_num, assigned_arm_id=selected.id, assigned_arm_name=selected.name, randomized_by=current_user.id, is_locked=True)
    db.add(randomization)
    p.status = "RANDOMIZED"
    await db.commit()
    await db.refresh(randomization)
    return randomization
''')

w("app/api/v1/visits.py", '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.visit import VisitDefinition, ParticipantVisit
from app.schemas.visit import VisitDefinitionCreate, ParticipantVisitCreate, ParticipantVisitUpdate, VisitDefinitionOut, ParticipantVisitOut
from typing import List, Optional

router = APIRouter(prefix="/visits", tags=["Visits"])

@router.get("/definitions", response_model=List[VisitDefinitionOut])
async def list_visit_definitions(trial_id: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(VisitDefinition)
    if trial_id:
        query = query.where(VisitDefinition.trial_id == trial_id)
    result = await db.execute(query.order_by(VisitDefinition.visit_number))
    return result.scalars().all()

@router.post("/definitions", response_model=VisitDefinitionOut)
async def create_visit_definition(data: VisitDefinitionCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN"))):
    vd = VisitDefinition(**data.model_dump())
    db.add(vd)
    await db.commit()
    await db.refresh(vd)
    return vd

@router.get("/", response_model=List[ParticipantVisitOut])
async def list_participant_visits(participant_id: Optional[str] = None, status: Optional[str] = None, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(ParticipantVisit)
    if participant_id:
        query = query.where(ParticipantVisit.participant_id == participant_id)
    if status:
        query = query.where(ParticipantVisit.status == status)
    result = await db.execute(query.offset(skip).limit(limit))
    return result.scalars().all()

@router.post("/", response_model=ParticipantVisitOut)
async def create_participant_visit(data: ParticipantVisitCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "PRINCIPAL_INVESTIGATOR", "STUDY_COORDINATOR"))):
    visit = ParticipantVisit(**data.model_dump())
    db.add(visit)
    await db.commit()
    await db.refresh(visit)
    return visit

@router.put("/{visit_id}", response_model=ParticipantVisitOut)
async def update_visit(visit_id: str, data: ParticipantVisitUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "PRINCIPAL_INVESTIGATOR", "STUDY_COORDINATOR"))):
    result = await db.execute(select(ParticipantVisit).where(ParticipantVisit.id == visit_id))
    visit = result.scalar_one_or_none()
    if not visit:
        raise HTTPException(status_code=404, detail="Visit not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(visit, key, value)
    await db.commit()
    return visit
''')

w("app/api/v1/forms.py", '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.form import Form, FormField, FormSubmission, DataQuery
from app.schemas.form import FormCreate, FormFieldCreate, FormSubmissionCreate, FormSubmissionUpdate, DataQueryCreate, DataQueryUpdate, FormOut, FormFieldOut, FormSubmissionOut, DataQueryOut
from typing import List, Optional
from datetime import datetime, timezone

router = APIRouter(prefix="/forms", tags=["eCRF / Forms"])

@router.get("/", response_model=List[FormOut])
async def list_forms(trial_id: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(Form).where(Form.is_deleted == False)
    if trial_id:
        query = query.where(Form.trial_id == trial_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/", response_model=FormOut)
async def create_form(data: FormCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN", "DATA_MANAGER"))):
    form = Form(**data.model_dump())
    db.add(form)
    await db.commit()
    await db.refresh(form)
    return form

@router.get("/{form_id}/fields", response_model=List[FormFieldOut])
async def get_form_fields(form_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(FormField).where(FormField.form_id == form_id).order_by(FormField.order_index))
    return result.scalars().all()

@router.post("/fields", response_model=FormFieldOut)
async def create_form_field(data: FormFieldCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN", "DATA_MANAGER"))):
    field = FormField(**data.model_dump())
    db.add(field)
    await db.commit()
    await db.refresh(field)
    return field

@router.get("/submissions", response_model=List[FormSubmissionOut])
async def list_submissions(form_id: Optional[str] = None, participant_id: Optional[str] = None, status: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(FormSubmission)
    if form_id:
        query = query.where(FormSubmission.form_id == form_id)
    if participant_id:
        query = query.where(FormSubmission.participant_id == participant_id)
    if status:
        query = query.where(FormSubmission.status == status)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/submissions", response_model=FormSubmissionOut)
async def create_submission(data: FormSubmissionCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "PRINCIPAL_INVESTIGATOR", "STUDY_COORDINATOR", "DATA_MANAGER"))):
    sub = FormSubmission(**data.model_dump(), submitted_by=current_user.id, submitted_at=datetime.now(timezone.utc))
    db.add(sub)
    await db.commit()
    await db.refresh(sub)
    return sub

@router.put("/submissions/{submission_id}", response_model=FormSubmissionOut)
async def update_submission(submission_id: str, data: FormSubmissionUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "PRINCIPAL_INVESTIGATOR", "STUDY_COORDINATOR", "DATA_MANAGER"))):
    result = await db.execute(select(FormSubmission).where(FormSubmission.id == submission_id))
    sub = result.scalar_one_or_none()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(sub, key, value)
    await db.commit()
    return sub

@router.get("/queries", response_model=List[DataQueryOut])
async def list_data_queries(status: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(DataQuery)
    if status:
        query = query.where(DataQuery.status == status)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/queries", response_model=DataQueryOut)
async def create_data_query(data: DataQueryCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "DATA_MANAGER"))):
    dq = DataQuery(**data.model_dump(), raised_by=current_user.id)
    db.add(dq)
    await db.commit()
    await db.refresh(dq)
    return dq

@router.put("/queries/{query_id}", response_model=DataQueryOut)
async def update_data_query(query_id: str, data: DataQueryUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(DataQuery).where(DataQuery.id == query_id))
    dq = result.scalar_one_or_none()
    if not dq:
        raise HTTPException(status_code=404, detail="Query not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(dq, key, value)
    if data.status == "RESOLVED":
        dq.resolved_at = datetime.now(timezone.utc)
    await db.commit()
    return dq
''')

w("app/api/v1/ethics.py", '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import date
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.ethics import EthicsCommittee, EthicsSubmission, EthicsApproval, EthicsReview, ProtocolAmendment
from app.schemas.ethics import EthicsCommitteeCreate, EthicsSubmissionCreate, EthicsSubmissionUpdate, EthicsApprovalCreate, EthicsSubmissionOut, EthicsApprovalOut, EthicsCommitteeOut
from typing import List, Optional

router = APIRouter(prefix="/ethics", tags=["Ethics"])

@router.get("/committees", response_model=List[EthicsCommitteeOut])
async def list_committees(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(EthicsCommittee))
    return result.scalars().all()

@router.post("/committees", response_model=EthicsCommitteeOut)
async def create_committee(data: EthicsCommitteeCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN", "ETHICS_COMMITTEE"))):
    ec = EthicsCommittee(**data.model_dump())
    db.add(ec)
    await db.commit()
    await db.refresh(ec)
    return ec

@router.get("/submissions", response_model=List[EthicsSubmissionOut])
async def list_submissions(trial_id: Optional[str] = None, status: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(EthicsSubmission)
    if trial_id:
        query = query.where(EthicsSubmission.trial_id == trial_id)
    if status:
        query = query.where(EthicsSubmission.status == status)
    result = await db.execute(query.order_by(EthicsSubmission.created_at.desc()))
    return result.scalars().all()

@router.post("/submissions", response_model=EthicsSubmissionOut)
async def create_submission(data: EthicsSubmissionCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN", "ETHICS_COMMITTEE"))):
    sub = EthicsSubmission(**data.model_dump(), submitted_by=current_user.id, submission_date=date.today(), status="SUBMITTED")
    db.add(sub)
    await db.commit()
    await db.refresh(sub)
    return sub

@router.put("/submissions/{submission_id}", response_model=EthicsSubmissionOut)
async def update_submission(submission_id: str, data: EthicsSubmissionUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "ETHICS_COMMITTEE"))):
    result = await db.execute(select(EthicsSubmission).where(EthicsSubmission.id == submission_id))
    sub = result.scalar_one_or_none()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(sub, key, value)
    await db.commit()
    return sub

@router.post("/approvals", response_model=EthicsApprovalOut)
async def create_approval(data: EthicsApprovalCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "ETHICS_COMMITTEE"))):
    approval = EthicsApproval(**data.model_dump())
    db.add(approval)
    # Update submission status
    result = await db.execute(select(EthicsSubmission).where(EthicsSubmission.id == data.submission_id))
    sub = result.scalar_one_or_none()
    if sub:
        sub.status = "APPROVED"
    await db.commit()
    await db.refresh(approval)
    return approval

@router.get("/approvals", response_model=List[EthicsApprovalOut])
async def list_approvals(trial_id: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(EthicsApproval)
    if trial_id:
        query = query.where(EthicsApproval.trial_id == trial_id)
    result = await db.execute(query)
    return result.scalars().all()
''')

w("app/api/v1/regulatory.py", '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.regulatory import RegulatoryRecord, RegulatoryChecklist
from app.schemas.regulatory import RegulatoryRecordCreate, RegulatoryRecordUpdate, RegulatoryChecklistCreate, RegulatoryChecklistUpdate, RegulatoryRecordOut, RegulatoryChecklistOut
from typing import List, Optional

router = APIRouter(prefix="/regulatory", tags=["Regulatory"])

@router.get("/records", response_model=List[RegulatoryRecordOut])
async def list_records(trial_id: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(RegulatoryRecord)
    if trial_id:
        query = query.where(RegulatoryRecord.trial_id == trial_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/records", response_model=RegulatoryRecordOut)
async def create_record(data: RegulatoryRecordCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "REGULATORY_OFFICER"))):
    record = RegulatoryRecord(**data.model_dump(), responsible_officer_id=current_user.id)
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record

@router.put("/records/{record_id}", response_model=RegulatoryRecordOut)
async def update_record(record_id: str, data: RegulatoryRecordUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "REGULATORY_OFFICER"))):
    result = await db.execute(select(RegulatoryRecord).where(RegulatoryRecord.id == record_id))
    record = result.scalar_one_or_none()
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(record, key, value)
    await db.commit()
    return record

@router.get("/checklists", response_model=List[RegulatoryChecklistOut])
async def list_checklists(trial_id: Optional[str] = None, category: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(RegulatoryChecklist)
    if trial_id:
        query = query.where(RegulatoryChecklist.trial_id == trial_id)
    if category:
        query = query.where(RegulatoryChecklist.category == category)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/checklists", response_model=RegulatoryChecklistOut)
async def create_checklist_item(data: RegulatoryChecklistCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "REGULATORY_OFFICER"))):
    item = RegulatoryChecklist(**data.model_dump())
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item

@router.put("/checklists/{item_id}", response_model=RegulatoryChecklistOut)
async def update_checklist_item(item_id: str, data: RegulatoryChecklistUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "REGULATORY_OFFICER"))):
    result = await db.execute(select(RegulatoryChecklist).where(RegulatoryChecklist.id == item_id))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Checklist item not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    if data.is_completed:
        from datetime import date as dt_date
        item.completed_by = current_user.id
        item.completed_date = dt_date.today()
    await db.commit()
    return item
''')

w("app/api/v1/pharmacovigilance.py", '''
import random, string
from datetime import date
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.pharmacovigilance import AdverseEvent, SeriousAdverseEvent, CausalityAssessment, SafetySignal
from app.schemas.pharmacovigilance import AdverseEventCreate, AdverseEventUpdate, SAECreate, SAEUpdate, CausalityAssessmentCreate, AdverseEventOut, SAEOut, SafetySignalOut
from typing import List, Optional

router = APIRouter(prefix="/pharmacovigilance", tags=["Pharmacovigilance"])

@router.get("/adverse-events", response_model=List[AdverseEventOut])
async def list_aes(trial_id: Optional[str] = None, severity: Optional[str] = None, seriousness: Optional[str] = None, status: Optional[str] = None, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(AdverseEvent).where(AdverseEvent.is_deleted == False)
    if trial_id:
        query = query.where(AdverseEvent.trial_id == trial_id)
    if severity:
        query = query.where(AdverseEvent.severity == severity)
    if seriousness:
        query = query.where(AdverseEvent.seriousness == seriousness)
    if status:
        query = query.where(AdverseEvent.status == status)
    result = await db.execute(query.order_by(AdverseEvent.reported_date.desc()).offset(skip).limit(limit))
    return result.scalars().all()

@router.post("/adverse-events", response_model=AdverseEventOut)
async def create_ae(data: AdverseEventCreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "PRINCIPAL_INVESTIGATOR", "STUDY_COORDINATOR", "PHARMACOVIGILANCE_OFFICER"))):
    ae = AdverseEvent(**data.model_dump(), reporter_id=current_user.id, reported_date=date.today(), status="REPORTED")
    db.add(ae)
    await db.commit()
    await db.refresh(ae)
    return ae

@router.put("/adverse-events/{ae_id}", response_model=AdverseEventOut)
async def update_ae(ae_id: str, data: AdverseEventUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "PRINCIPAL_INVESTIGATOR", "PHARMACOVIGILANCE_OFFICER"))):
    result = await db.execute(select(AdverseEvent).where(AdverseEvent.id == ae_id))
    ae = result.scalar_one_or_none()
    if not ae:
        raise HTTPException(status_code=404, detail="Adverse event not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(ae, key, value)
    await db.commit()
    return ae

@router.get("/serious-adverse-events", response_model=List[SAEOut])
async def list_saes(status: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(SeriousAdverseEvent)
    if status:
        query = query.where(SeriousAdverseEvent.status == status)
    result = await db.execute(query)
    return result.scalars().all()

@router.post("/serious-adverse-events", response_model=SAEOut)
async def create_sae(data: SAECreate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "PRINCIPAL_INVESTIGATOR", "PHARMACOVIGILANCE_OFFICER"))):
    sae_num = "SAE-" + "".join(random.choices(string.digits, k=6))
    sae = SeriousAdverseEvent(**data.model_dump(), sae_number=sae_num, status="REPORTED")
    db.add(sae)
    # Update AE seriousness
    result = await db.execute(select(AdverseEvent).where(AdverseEvent.id == data.adverse_event_id))
    ae = result.scalar_one_or_none()
    if ae:
        ae.seriousness = "SERIOUS"
    await db.commit()
    await db.refresh(sae)
    return sae

@router.put("/serious-adverse-events/{sae_id}", response_model=SAEOut)
async def update_sae(sae_id: str, data: SAEUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "PHARMACOVIGILANCE_OFFICER"))):
    result = await db.execute(select(SeriousAdverseEvent).where(SeriousAdverseEvent.id == sae_id))
    sae = result.scalar_one_or_none()
    if not sae:
        raise HTTPException(status_code=404, detail="SAE not found")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(sae, key, value)
    await db.commit()
    return sae

@router.get("/safety-signals", response_model=List[SafetySignalOut])
async def list_safety_signals(trial_id: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(SafetySignal)
    if trial_id:
        query = query.where(SafetySignal.trial_id == trial_id)
    result = await db.execute(query)
    return result.scalars().all()

@router.get("/summary")
async def safety_summary(trial_id: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    ae_q = select(func.count()).select_from(AdverseEvent).where(AdverseEvent.is_deleted == False)
    sae_q = select(func.count()).select_from(SeriousAdverseEvent)
    if trial_id:
        ae_q = ae_q.where(AdverseEvent.trial_id == trial_id)
    total_aes = (await db.execute(ae_q)).scalar() or 0
    total_saes = (await db.execute(sae_q)).scalar() or 0
    open_saes = (await db.execute(select(func.count()).select_from(SeriousAdverseEvent).where(SeriousAdverseEvent.status != "CLOSED"))).scalar() or 0
    # Severity breakdown
    mild = (await db.execute(select(func.count()).select_from(AdverseEvent).where(AdverseEvent.severity == "MILD"))).scalar() or 0
    moderate = (await db.execute(select(func.count()).select_from(AdverseEvent).where(AdverseEvent.severity == "MODERATE"))).scalar() or 0
    severe = (await db.execute(select(func.count()).select_from(AdverseEvent).where(AdverseEvent.severity == "SEVERE"))).scalar() or 0
    return {"total_aes": total_aes, "total_saes": total_saes, "open_saes": open_saes, "by_severity": {"mild": mild, "moderate": moderate, "severe": severe}}
''')

w("app/api/v1/documents.py", '''
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form as FastAPIForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.document import Document
from app.schemas.document import DocumentOut
from typing import List, Optional
import os, uuid

router = APIRouter(prefix="/documents", tags=["Documents"])

STORAGE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), "storage")

@router.get("/", response_model=List[DocumentOut])
async def list_documents(trial_id: Optional[str] = None, document_type: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(Document).where(Document.is_deleted == False)
    if trial_id:
        query = query.where(Document.trial_id == trial_id)
    if document_type:
        query = query.where(Document.document_type == document_type)
    result = await db.execute(query.order_by(Document.created_at.desc()))
    return result.scalars().all()

@router.post("/upload", response_model=DocumentOut)
async def upload_document(title: str = FastAPIForm(...), document_type: str = FastAPIForm("OTHER"), trial_id: Optional[str] = FastAPIForm(None), description: Optional[str] = FastAPIForm(None), file: UploadFile = File(...), db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "TRIAL_ADMIN", "PRINCIPAL_INVESTIGATOR", "STUDY_COORDINATOR", "DATA_MANAGER", "REGULATORY_OFFICER"))):
    # Validate file type
    blocked = [".exe", ".bat", ".cmd", ".sh", ".ps1", ".vbs", ".js"]
    ext = os.path.splitext(file.filename or "")[1].lower()
    if ext in blocked:
        raise HTTPException(status_code=400, detail="Executable files not allowed")
    # Save file
    os.makedirs(STORAGE_PATH, exist_ok=True)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(STORAGE_PATH, f"{file_id}{ext}")
    content = await file.read()
    with open(file_path, "wb") as f:
        f.write(content)
    doc = Document(trial_id=trial_id, title=title, document_type=document_type, file_name=file.filename, file_path=file_path, file_size=len(content), mime_type=file.content_type, uploaded_by=current_user.id, description=description)
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc
''')

w("app/api/v1/audit.py", '''
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.audit import AuditLog
from app.schemas.audit import AuditLogOut
from typing import List, Optional

router = APIRouter(prefix="/audit", tags=["Audit"])

@router.get("/", response_model=List[AuditLogOut])
async def list_audit_logs(entity_type: Optional[str] = None, action: Optional[str] = None, user_id: Optional[str] = None, skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "AUDITOR"))):
    query = select(AuditLog)
    if entity_type:
        query = query.where(AuditLog.entity_type == entity_type)
    if action:
        query = query.where(AuditLog.action == action)
    if user_id:
        query = query.where(AuditLog.user_id == user_id)
    result = await db.execute(query.order_by(AuditLog.timestamp.desc()).offset(skip).limit(limit))
    return result.scalars().all()
''')

w("app/api/v1/notifications.py", '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, update
from datetime import datetime, timezone
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.notification import Notification
from app.schemas.notification import NotificationOut
from typing import List

router = APIRouter(prefix="/notifications", tags=["Notifications"])

@router.get("/", response_model=List[NotificationOut])
async def list_notifications(is_read: bool = None, skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    query = select(Notification).where(Notification.user_id == current_user.id)
    if is_read is not None:
        query = query.where(Notification.is_read == is_read)
    result = await db.execute(query.order_by(Notification.created_at.desc()).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/unread-count")
async def unread_count(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(func.count()).select_from(Notification).where(Notification.user_id == current_user.id, Notification.is_read == False))
    return {"count": result.scalar() or 0}

@router.put("/{notification_id}/read")
async def mark_as_read(notification_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Notification).where(Notification.id == notification_id, Notification.user_id == current_user.id))
    notif = result.scalar_one_or_none()
    if notif:
        notif.is_read = True
        notif.read_at = datetime.now(timezone.utc)
        await db.commit()
    return {"status": "ok"}

@router.put("/read-all")
async def mark_all_read(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    await db.execute(update(Notification).where(Notification.user_id == current_user.id, Notification.is_read == False).values(is_read=True, read_at=datetime.now(timezone.utc)))
    await db.commit()
    return {"status": "ok"}
''')

w("app/api/v1/analytics.py", '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.trial import Trial
from app.models.site import Site, SiteAssignment
from app.models.participant import Participant
from app.models.visit import ParticipantVisit
from app.models.form import DataQuery
from app.models.pharmacovigilance import AdverseEvent, SeriousAdverseEvent
from app.models.ethics import EthicsSubmission, EthicsApproval
from app.models.regulatory import RegulatoryRecord
from app.models.audit import AuditLog
from app.schemas.analytics import DashboardKPIs, DashboardData, ChartData
from typing import Optional

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/dashboard")
async def get_dashboard(trial_id: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    # KPIs
    active_trials = (await db.execute(select(func.count()).select_from(Trial).where(Trial.status.in_(["ACTIVE", "RECRUITING"])))).scalar() or 0
    recruiting_trials = (await db.execute(select(func.count()).select_from(Trial).where(Trial.status == "RECRUITING"))).scalar() or 0
    total_participants = (await db.execute(select(func.count()).select_from(Participant).where(Participant.is_deleted == False))).scalar() or 0
    active_sites = (await db.execute(select(func.count()).select_from(Site).where(Site.status == "ACTIVE"))).scalar() or 0
    
    total_visits = (await db.execute(select(func.count()).select_from(ParticipantVisit))).scalar() or 1
    completed_visits = (await db.execute(select(func.count()).select_from(ParticipantVisit).where(ParticipantVisit.status == "COMPLETED"))).scalar() or 0
    overdue_visits = (await db.execute(select(func.count()).select_from(ParticipantVisit).where(ParticipantVisit.status == "OVERDUE"))).scalar() or 0
    visit_compliance = round((completed_visits / max(total_visits, 1)) * 100, 1)
    
    open_queries = (await db.execute(select(func.count()).select_from(DataQuery).where(DataQuery.status == "OPEN"))).scalar() or 0
    open_saes = (await db.execute(select(func.count()).select_from(SeriousAdverseEvent).where(SeriousAdverseEvent.status != "CLOSED"))).scalar() or 0
    pending_ethics = (await db.execute(select(func.count()).select_from(EthicsSubmission).where(EthicsSubmission.status.in_(["SUBMITTED", "UNDER_REVIEW"])))).scalar() or 0
    reg_due = (await db.execute(select(func.count()).select_from(RegulatoryRecord).where(RegulatoryRecord.status.in_(["PREPARING", "SUBMITTED", "UPDATE_REQUIRED"])))).scalar() or 0
    total_aes = (await db.execute(select(func.count()).select_from(AdverseEvent))).scalar() or 0
    
    enrolled = (await db.execute(select(func.count()).select_from(Participant).where(Participant.status.in_(["ENROLLED", "RANDOMIZED", "ACTIVE", "COMPLETED"])))).scalar() or 0
    total_trials = (await db.execute(select(func.count()).select_from(Trial))).scalar() or 1
    enrollment_rate = round((enrolled / max(total_participants, 1)) * 100, 1) if total_participants > 0 else 0.0
    
    kpis = {
        "active_trials": active_trials,
        "recruiting_trials": recruiting_trials,
        "total_participants": total_participants,
        "active_sites": active_sites,
        "enrollment_rate": enrollment_rate,
        "visit_compliance": visit_compliance,
        "open_data_queries": open_queries,
        "open_saes": open_saes,
        "pending_ethics": pending_ethics,
        "regulatory_items_due": reg_due,
        "total_aes": total_aes,
        "completed_visits": completed_visits,
        "overdue_visits": overdue_visits,
    }
    
    # Trial status distribution
    status_counts = {}
    statuses = ["PLANNING", "ETHICS_PENDING", "ETHICS_APPROVED", "RECRUITING", "ACTIVE", "COMPLETED", "SUSPENDED"]
    for s in statuses:
        c = (await db.execute(select(func.count()).select_from(Trial).where(Trial.status == s))).scalar() or 0
        if c > 0:
            status_counts[s] = c
    
    trial_status = {
        "labels": list(status_counts.keys()),
        "datasets": [{"data": list(status_counts.values()), "label": "Trials"}]
    }
    
    # Enrollment by site
    sites_r = await db.execute(select(Site).where(Site.status == "ACTIVE").limit(10))
    sites = sites_r.scalars().all()
    site_names = []
    site_counts = []
    for s in sites:
        pc = (await db.execute(select(func.count()).select_from(Participant).where(Participant.site_id == s.id))).scalar() or 0
        site_names.append(s.name[:20])
        site_counts.append(pc)
    
    enrollment_by_site = {
        "labels": site_names,
        "datasets": [{"data": site_counts, "label": "Enrolled"}]
    }
    
    # Participant funnel
    screened = (await db.execute(select(func.count()).select_from(Participant))).scalar() or 0
    consented = (await db.execute(select(func.count()).select_from(Participant).where(Participant.status.in_(["CONSENTED", "ENROLLED", "RANDOMIZED", "ACTIVE", "COMPLETED"])))).scalar() or 0
    randomized = (await db.execute(select(func.count()).select_from(Participant).where(Participant.status.in_(["RANDOMIZED", "ACTIVE", "COMPLETED"])))).scalar() or 0
    completed_p = (await db.execute(select(func.count()).select_from(Participant).where(Participant.status == "COMPLETED"))).scalar() or 0
    
    participant_funnel = {
        "labels": ["Screened", "Consented", "Enrolled", "Randomized", "Completed"],
        "datasets": [{"data": [screened, consented, enrolled, randomized, completed_p], "label": "Participants"}]
    }
    
    # AE severity breakdown
    ae_severity = {
        "labels": ["Mild", "Moderate", "Severe"],
        "datasets": [{"data": [
            (await db.execute(select(func.count()).select_from(AdverseEvent).where(AdverseEvent.severity == "MILD"))).scalar() or 0,
            (await db.execute(select(func.count()).select_from(AdverseEvent).where(AdverseEvent.severity == "MODERATE"))).scalar() or 0,
            (await db.execute(select(func.count()).select_from(AdverseEvent).where(AdverseEvent.severity == "SEVERE"))).scalar() or 0,
        ], "label": "AEs"}]
    }
    
    # Recent activity
    recent_r = await db.execute(select(AuditLog).order_by(AuditLog.timestamp.desc()).limit(10))
    recent = [{"action": a.action, "entity_type": a.entity_type, "user_email": a.user_email, "timestamp": str(a.timestamp), "details": a.details} for a in recent_r.scalars().all()]
    
    # Upcoming deadlines from ethics approvals
    from datetime import date
    approvals_r = await db.execute(select(EthicsApproval).where(EthicsApproval.valid_until != None).order_by(EthicsApproval.valid_until).limit(5))
    deadlines = [{"type": "Ethics Renewal", "date": str(a.valid_until), "trial_id": a.trial_id, "detail": f"Approval {a.approval_number} expires"} for a in approvals_r.scalars().all()]
    
    return {
        "kpis": kpis,
        "trial_status_distribution": trial_status,
        "enrollment_by_site": enrollment_by_site,
        "participant_funnel": participant_funnel,
        "ae_trend": ae_severity,
        "recruitment_trend": {"labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], "datasets": [{"data": [5, 12, 18, 25, 35, 42], "label": "Cumulative Enrollment"}]},
        "visit_compliance_data": {"labels": ["Completed", "Scheduled", "Missed", "Overdue"], "datasets": [{"data": [completed_visits, total_visits - completed_visits - overdue_visits, 0, overdue_visits], "label": "Visits"}]},
        "site_performance": enrollment_by_site,
        "recent_activity": recent,
        "upcoming_deadlines": deadlines,
    }
''')

w("app/api/v1/cdisc.py", '''
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.cdisc import CDISCMapping
from app.models.participant import Participant
from app.models.visit import ParticipantVisit
from app.models.pharmacovigilance import AdverseEvent
from app.schemas.cdisc import CDISCMappingOut, CDISCExportRequest
from typing import List
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/cdisc", tags=["CDISC"])

@router.get("/mappings", response_model=List[CDISCMappingOut])
async def list_mappings(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(CDISCMapping).where(CDISCMapping.is_active == True))
    return result.scalars().all()

@router.post("/export")
async def export_cdisc(request: CDISCExportRequest, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "DATA_MANAGER"))):
    export_data = {}
    
    if "DM" in request.domains:
        # Demographics domain
        participants_r = await db.execute(select(Participant).where(Participant.trial_id == request.trial_id, Participant.is_deleted == False))
        participants = participants_r.scalars().all()
        dm_records = []
        for p in participants:
            dm_records.append({
                "STUDYID": request.trial_id[:8],
                "DOMAIN": "DM",
                "USUBJID": p.participant_id,
                "SUBJID": p.participant_id,
                "RFSTDTC": str(p.enrollment_date) if p.enrollment_date else "",
                "AGE": p.age,
                "SEX": p.gender[0].upper() if p.gender else "",
                "ARMCD": p.status,
            })
        export_data["DM"] = dm_records
    
    if "SV" in request.domains:
        # Subject visits domain
        visits_r = await db.execute(select(ParticipantVisit).join(Participant).where(Participant.trial_id == request.trial_id))
        visits = visits_r.scalars().all()
        sv_records = []
        for v in visits:
            sv_records.append({
                "STUDYID": request.trial_id[:8],
                "DOMAIN": "SV",
                "USUBJID": v.participant_id,
                "VISIT": v.visit_name or "",
                "SVSTDTC": str(v.actual_date) if v.actual_date else str(v.scheduled_date) if v.scheduled_date else "",
                "SVSTAT": v.status,
            })
        export_data["SV"] = sv_records
    
    if "AE" in request.domains:
        # Adverse events domain
        aes_r = await db.execute(select(AdverseEvent).where(AdverseEvent.trial_id == request.trial_id))
        aes = aes_r.scalars().all()
        ae_records = []
        for ae in aes:
            ae_records.append({
                "STUDYID": request.trial_id[:8],
                "DOMAIN": "AE",
                "USUBJID": ae.participant_id,
                "AETERM": ae.event_term,
                "AESEV": ae.severity,
                "AESER": "Y" if ae.seriousness == "SERIOUS" else "N",
                "AEREL": ae.causality,
                "AESTDTC": str(ae.onset_date) if ae.onset_date else "",
                "AEENDTC": str(ae.resolution_date) if ae.resolution_date else "",
                "AEOUT": ae.outcome,
            })
        export_data["AE"] = ae_records
    
    return JSONResponse(content=export_data)
''')

w("app/api/v1/fhir.py", '''
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.participant import Participant
from app.models.trial import Trial
from app.models.pharmacovigilance import AdverseEvent
from app.models.visit import ParticipantVisit
from typing import Optional

router = APIRouter(prefix="/fhir", tags=["FHIR R4"])

@router.get("/Patient/{patient_id}")
async def get_patient(patient_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Participant).where(Participant.id == patient_id))
    p = result.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {
        "resourceType": "Patient",
        "id": p.id,
        "identifier": [{"system": "urn:aiia:participant", "value": p.participant_id}],
        "gender": p.gender or "unknown",
        "meta": {"versionId": "1", "lastUpdated": str(p.updated_at)},
    }

@router.get("/ResearchStudy/{study_id}")
async def get_research_study(study_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Trial).where(Trial.id == study_id))
    t = result.scalar_one_or_none()
    if not t:
        raise HTTPException(status_code=404, detail="Study not found")
    fhir_status_map = {"PLANNING": "in-review", "RECRUITING": "active", "ACTIVE": "active", "COMPLETED": "completed", "SUSPENDED": "temporarily-closed-to-accrual"}
    return {
        "resourceType": "ResearchStudy",
        "id": t.id,
        "identifier": [{"system": "urn:aiia:trial", "value": t.protocol_number or t.id}],
        "title": t.title,
        "status": fhir_status_map.get(t.status, "in-review"),
        "phase": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/research-study-phase", "code": (t.phase or "n-a").lower().replace(" ", "-")}]},
        "description": t.primary_objective,
    }

@router.get("/ResearchSubject/{subject_id}")
async def get_research_subject(subject_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Participant).where(Participant.id == subject_id))
    p = result.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail="Subject not found")
    fhir_status_map = {"SCREENED": "candidate", "ENROLLED": "on-study", "RANDOMIZED": "on-study", "ACTIVE": "on-study", "COMPLETED": "off-study", "WITHDRAWN": "withdrawn"}
    return {
        "resourceType": "ResearchSubject",
        "id": p.id,
        "status": fhir_status_map.get(p.status, "candidate"),
        "study": {"reference": f"ResearchStudy/{p.trial_id}"},
        "individual": {"reference": f"Patient/{p.id}"},
    }

@router.get("/Observation/{observation_id}")
async def get_observation(observation_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(ParticipantVisit).where(ParticipantVisit.id == observation_id))
    v = result.scalar_one_or_none()
    if not v:
        raise HTTPException(status_code=404, detail="Observation not found")
    return {
        "resourceType": "Observation",
        "id": v.id,
        "status": "final" if v.status == "COMPLETED" else "registered",
        "code": {"coding": [{"system": "urn:aiia:visit", "code": v.visit_name or "visit"}]},
        "subject": {"reference": f"Patient/{v.participant_id}"},
        "effectiveDateTime": str(v.actual_date) if v.actual_date else str(v.scheduled_date),
    }

@router.get("/AdverseEvent/{ae_id}")
async def get_adverse_event(ae_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(AdverseEvent).where(AdverseEvent.id == ae_id))
    ae = result.scalar_one_or_none()
    if not ae:
        raise HTTPException(status_code=404, detail="Adverse event not found")
    return {
        "resourceType": "AdverseEvent",
        "id": ae.id,
        "actuality": "actual",
        "event": {"coding": [{"system": "urn:aiia:ae", "display": ae.event_term}]},
        "subject": {"reference": f"Patient/{ae.participant_id}"},
        "date": str(ae.onset_date) if ae.onset_date else None,
        "seriousness": {"coding": [{"display": ae.seriousness}]},
        "severity": {"coding": [{"display": ae.severity}]},
    }
''')

w("app/api/v1/search.py", '''
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.trial import Trial
from app.models.participant import Participant
from app.models.site import Site, Investigator
from app.models.pharmacovigilance import AdverseEvent
from app.models.document import Document

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/")
async def global_search(q: str = Query(..., min_length=2), db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    results = []
    pattern = f"%{q}%"
    
    # Trials
    trials_r = await db.execute(select(Trial).where(or_(Trial.title.ilike(pattern), Trial.protocol_number.ilike(pattern), Trial.short_title.ilike(pattern))).limit(5))
    for t in trials_r.scalars().all():
        results.append({"type": "trial", "id": t.id, "title": t.title, "subtitle": t.protocol_number, "status": t.status})
    
    # Participants
    parts_r = await db.execute(select(Participant).where(Participant.participant_id.ilike(pattern)).limit(5))
    for p in parts_r.scalars().all():
        results.append({"type": "participant", "id": p.id, "title": p.participant_id, "subtitle": p.status, "status": p.status})
    
    # Sites
    sites_r = await db.execute(select(Site).where(or_(Site.name.ilike(pattern), Site.city.ilike(pattern))).limit(5))
    for s in sites_r.scalars().all():
        results.append({"type": "site", "id": s.id, "title": s.name, "subtitle": s.city, "status": s.status})
    
    # Investigators
    inv_r = await db.execute(select(Investigator).where(Investigator.name.ilike(pattern)).limit(5))
    for i in inv_r.scalars().all():
        results.append({"type": "investigator", "id": i.id, "title": i.name, "subtitle": i.specialization})
    
    # Documents
    docs_r = await db.execute(select(Document).where(Document.title.ilike(pattern)).limit(5))
    for d in docs_r.scalars().all():
        results.append({"type": "document", "id": d.id, "title": d.title, "subtitle": d.document_type})
    
    # AEs
    aes_r = await db.execute(select(AdverseEvent).where(AdverseEvent.event_term.ilike(pattern)).limit(5))
    for ae in aes_r.scalars().all():
        results.append({"type": "adverse_event", "id": ae.id, "title": ae.event_term, "subtitle": ae.severity, "status": ae.status})
    
    return {"results": results, "total": len(results)}
''')

# ==============================================================
# ROUTER
# ==============================================================
w("app/api/v1/router.py", '''
from fastapi import APIRouter
from app.api.v1 import auth, users, trials, sites, participants, visits, forms, ethics, regulatory, pharmacovigilance, documents, audit, notifications, analytics, cdisc, fhir, search

api_router = APIRouter()

api_router.include_router(auth.router)
api_router.include_router(users.router)
api_router.include_router(trials.router)
api_router.include_router(sites.router)
api_router.include_router(participants.router)
api_router.include_router(visits.router)
api_router.include_router(forms.router)
api_router.include_router(ethics.router)
api_router.include_router(regulatory.router)
api_router.include_router(pharmacovigilance.router)
api_router.include_router(documents.router)
api_router.include_router(audit.router)
api_router.include_router(notifications.router)
api_router.include_router(analytics.router)
api_router.include_router(cdisc.router)
api_router.include_router(fhir.router)
api_router.include_router(search.router)
''')

# ==============================================================
# MAIN APP
# ==============================================================
w("app/main.py", '''
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.v1.router import api_router
from app.core.database import engine, Base
from contextlib import asynccontextmanager
import time, logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting AIIA CTMS API...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database tables created/verified.")
    yield
    logger.info("Shutting down AIIA CTMS API...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="AIIA Clinical Trials Dashboard - A comprehensive CTMS for Ayurveda research with CDISC/FHIR interoperability, role-based KPIs, ethics and regulatory tracking, and integrated pharmacovigilance.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    logger.info(f"{request.method} {request.url.path} - {response.status_code} - {duration:.3f}s")
    return response

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "AIIA CTMS API", "version": settings.VERSION}

@app.get("/ready")
async def readiness_check():
    return {"status": "ready"}
''')

print("Part 3 (API Routes + Main) generated successfully.")
