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
