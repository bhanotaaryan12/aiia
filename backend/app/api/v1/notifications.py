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
