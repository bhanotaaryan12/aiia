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
