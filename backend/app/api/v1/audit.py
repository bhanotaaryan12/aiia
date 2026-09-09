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
