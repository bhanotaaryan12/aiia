from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import get_current_user, require_roles
from app.models.cdisc import CDISCMapping
from app.models.participant import Participant
from app.models.visit import ParticipantVisit
from app.models.pharmacovigilance import AdverseEvent
from app.schemas.cdisc import CDISCMappingOut, CDISCExportRequest
from typing import List
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/cdisc", tags=["CDISC"])

@router.get("/mappings", response_model=List[CDISCMappingOut])
async def list_mappings(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(CDISCMapping).where(CDISCMapping.is_active == True))
    return result.scalars().all()

@router.post("/export")
async def export_cdisc(request: CDISCExportRequest, db: AsyncSession = Depends(get_db), current_user = Depends(require_roles("SUPER_ADMIN", "DATA_MANAGER"))):
    export_data = {}
    
    if "DM" in request.domains:
        # Demographics domain
        participants_r = await db.execute(select(Participant).where(Participant.trial_id == request.trial_id, Participant.is_deleted == False))
        participants = participants_r.scalars().all()
        dm_records = []
        for p in participants:
            dm_records.append({
                "STUDYID": request.trial_id[:8],
                "DOMAIN": "DM",
                "USUBJID": p.participant_id,
                "SUBJID": p.participant_id,
                "RFSTDTC": str(p.enrollment_date) if p.enrollment_date else "",
                "AGE": p.age,
                "SEX": p.gender[0].upper() if p.gender else "",
                "ARMCD": p.status,
            })
        export_data["DM"] = dm_records
    
    if "SV" in request.domains:
        # Subject visits domain
        visits_r = await db.execute(select(ParticipantVisit).join(Participant).where(Participant.trial_id == request.trial_id))
        visits = visits_r.scalars().all()
        sv_records = []
        for v in visits:
            sv_records.append({
                "STUDYID": request.trial_id[:8],
                "DOMAIN": "SV",
                "USUBJID": v.participant_id,
                "VISIT": v.visit_name or "",
                "SVSTDTC": str(v.actual_date) if v.actual_date else str(v.scheduled_date) if v.scheduled_date else "",
                "SVSTAT": v.status,
            })
        export_data["SV"] = sv_records
    
    if "AE" in request.domains:
        # Adverse events domain
        aes_r = await db.execute(select(AdverseEvent).where(AdverseEvent.trial_id == request.trial_id))
        aes = aes_r.scalars().all()
        ae_records = []
        for ae in aes:
            ae_records.append({
                "STUDYID": request.trial_id[:8],
                "DOMAIN": "AE",
                "USUBJID": ae.participant_id,
                "AETERM": ae.event_term,
                "AESEV": ae.severity,
                "AESER": "Y" if ae.seriousness == "SERIOUS" else "N",
                "AEREL": ae.causality,
                "AESTDTC": str(ae.onset_date) if ae.onset_date else "",
                "AEENDTC": str(ae.resolution_date) if ae.resolution_date else "",
                "AEOUT": ae.outcome,
            })
        export_data["AE"] = ae_records
    
    return JSONResponse(content=export_data)
