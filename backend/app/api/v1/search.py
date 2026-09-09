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
