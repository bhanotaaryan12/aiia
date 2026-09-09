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
