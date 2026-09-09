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
