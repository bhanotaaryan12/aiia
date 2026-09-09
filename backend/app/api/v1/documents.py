from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form as FastAPIForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.config import settings
from app.core.security import get_current_user, require_roles
from app.models.document import Document
from app.schemas.document import DocumentOut
from typing import List, Optional
import os, re, uuid

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
    allowed_extensions = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".csv", ".txt"}
    allowed_types = {"application/pdf", "application/msword", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "application/vnd.ms-excel", "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", "text/csv", "text/plain"}
    original_name = os.path.basename(file.filename or "")
    ext = os.path.splitext(original_name)[1].lower()
    if ext not in allowed_extensions or file.content_type not in allowed_types:
        raise HTTPException(status_code=400, detail="Unsupported file type")
    content_length = int(file.headers.get("content-length", "0"))
    if content_length > settings.MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds the upload limit")
    content = await file.read(settings.MAX_UPLOAD_BYTES + 1)
    if len(content) > settings.MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=413, detail="File exceeds the upload limit")
    clean_title = re.sub(r"[\x00-\x1f\x7f]", "", title).strip()[:200]
    clean_description = re.sub(r"[\x00-\x1f\x7f]", "", description or "").strip()[:2000] or None
    if not clean_title:
        raise HTTPException(status_code=422, detail="A document title is required")
    os.makedirs(STORAGE_PATH, exist_ok=True)
    file_id = str(uuid.uuid4())
    file_path = os.path.join(STORAGE_PATH, f"{file_id}{ext}")
    with open(file_path, "wb") as f:
        f.write(content)
    doc = Document(trial_id=trial_id, title=clean_title, document_type=document_type, file_name=original_name, file_path=file_path, file_size=len(content), mime_type=file.content_type, uploaded_by=current_user.id, description=clean_description)
    db.add(doc)
    await db.commit()
    await db.refresh(doc)
    return doc
