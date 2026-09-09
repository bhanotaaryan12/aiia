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
