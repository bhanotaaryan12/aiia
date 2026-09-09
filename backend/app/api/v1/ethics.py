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
