from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.participant import Participant
from app.models.trial import Trial
from app.models.pharmacovigilance import AdverseEvent
from app.models.visit import ParticipantVisit
from typing import Optional

router = APIRouter(prefix="/fhir", tags=["FHIR R4"])

@router.get("/Patient/{patient_id}")
async def get_patient(patient_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Participant).where(Participant.id == patient_id))
    p = result.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail="Patient not found")
    return {
        "resourceType": "Patient",
        "id": p.id,
        "identifier": [{"system": "urn:aiia:participant", "value": p.participant_id}],
        "gender": p.gender or "unknown",
        "meta": {"versionId": "1", "lastUpdated": str(p.updated_at)},
    }

@router.get("/ResearchStudy/{study_id}")
async def get_research_study(study_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Trial).where(Trial.id == study_id))
    t = result.scalar_one_or_none()
    if not t:
        raise HTTPException(status_code=404, detail="Study not found")
    fhir_status_map = {"PLANNING": "in-review", "RECRUITING": "active", "ACTIVE": "active", "COMPLETED": "completed", "SUSPENDED": "temporarily-closed-to-accrual"}
    return {
        "resourceType": "ResearchStudy",
        "id": t.id,
        "identifier": [{"system": "urn:aiia:trial", "value": t.protocol_number or t.id}],
        "title": t.title,
        "status": fhir_status_map.get(t.status, "in-review"),
        "phase": {"coding": [{"system": "http://terminology.hl7.org/CodeSystem/research-study-phase", "code": (t.phase or "n-a").lower().replace(" ", "-")}]},
        "description": t.primary_objective,
    }

@router.get("/ResearchSubject/{subject_id}")
async def get_research_subject(subject_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(Participant).where(Participant.id == subject_id))
    p = result.scalar_one_or_none()
    if not p:
        raise HTTPException(status_code=404, detail="Subject not found")
    fhir_status_map = {"SCREENED": "candidate", "ENROLLED": "on-study", "RANDOMIZED": "on-study", "ACTIVE": "on-study", "COMPLETED": "off-study", "WITHDRAWN": "withdrawn"}
    return {
        "resourceType": "ResearchSubject",
        "id": p.id,
        "status": fhir_status_map.get(p.status, "candidate"),
        "study": {"reference": f"ResearchStudy/{p.trial_id}"},
        "individual": {"reference": f"Patient/{p.id}"},
    }

@router.get("/Observation/{observation_id}")
async def get_observation(observation_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(ParticipantVisit).where(ParticipantVisit.id == observation_id))
    v = result.scalar_one_or_none()
    if not v:
        raise HTTPException(status_code=404, detail="Observation not found")
    return {
        "resourceType": "Observation",
        "id": v.id,
        "status": "final" if v.status == "COMPLETED" else "registered",
        "code": {"coding": [{"system": "urn:aiia:visit", "code": v.visit_name or "visit"}]},
        "subject": {"reference": f"Patient/{v.participant_id}"},
        "effectiveDateTime": str(v.actual_date) if v.actual_date else str(v.scheduled_date),
    }

@router.get("/AdverseEvent/{ae_id}")
async def get_adverse_event(ae_id: str, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    result = await db.execute(select(AdverseEvent).where(AdverseEvent.id == ae_id))
    ae = result.scalar_one_or_none()
    if not ae:
        raise HTTPException(status_code=404, detail="Adverse event not found")
    return {
        "resourceType": "AdverseEvent",
        "id": ae.id,
        "actuality": "actual",
        "event": {"coding": [{"system": "urn:aiia:ae", "display": ae.event_term}]},
        "subject": {"reference": f"Patient/{ae.participant_id}"},
        "date": str(ae.onset_date) if ae.onset_date else None,
        "seriousness": {"coding": [{"display": ae.seriousness}]},
        "severity": {"coding": [{"display": ae.severity}]},
    }
