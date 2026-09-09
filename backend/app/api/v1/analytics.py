from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, extract
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.trial import Trial
from app.models.site import Site, SiteAssignment
from app.models.participant import Participant
from app.models.visit import ParticipantVisit
from app.models.form import DataQuery
from app.models.pharmacovigilance import AdverseEvent, SeriousAdverseEvent
from app.models.ethics import EthicsSubmission, EthicsApproval
from app.models.regulatory import RegulatoryRecord
from app.models.audit import AuditLog
from app.schemas.analytics import DashboardKPIs, DashboardData, ChartData
from typing import Optional

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/dashboard")
async def get_dashboard(trial_id: Optional[str] = None, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    # KPIs
    active_trials = (await db.execute(select(func.count()).select_from(Trial).where(Trial.status.in_(["ACTIVE", "RECRUITING"])))).scalar() or 0
    recruiting_trials = (await db.execute(select(func.count()).select_from(Trial).where(Trial.status == "RECRUITING"))).scalar() or 0
    total_participants = (await db.execute(select(func.count()).select_from(Participant).where(Participant.is_deleted == False))).scalar() or 0
    active_sites = (await db.execute(select(func.count()).select_from(Site).where(Site.status == "ACTIVE"))).scalar() or 0
    
    total_visits = (await db.execute(select(func.count()).select_from(ParticipantVisit))).scalar() or 1
    completed_visits = (await db.execute(select(func.count()).select_from(ParticipantVisit).where(ParticipantVisit.status == "COMPLETED"))).scalar() or 0
    overdue_visits = (await db.execute(select(func.count()).select_from(ParticipantVisit).where(ParticipantVisit.status == "OVERDUE"))).scalar() or 0
    visit_compliance = round((completed_visits / max(total_visits, 1)) * 100, 1)
    
    open_queries = (await db.execute(select(func.count()).select_from(DataQuery).where(DataQuery.status == "OPEN"))).scalar() or 0
    open_saes = (await db.execute(select(func.count()).select_from(SeriousAdverseEvent).where(SeriousAdverseEvent.status != "CLOSED"))).scalar() or 0
    pending_ethics = (await db.execute(select(func.count()).select_from(EthicsSubmission).where(EthicsSubmission.status.in_(["SUBMITTED", "UNDER_REVIEW"])))).scalar() or 0
    reg_due = (await db.execute(select(func.count()).select_from(RegulatoryRecord).where(RegulatoryRecord.status.in_(["PREPARING", "SUBMITTED", "UPDATE_REQUIRED"])))).scalar() or 0
    total_aes = (await db.execute(select(func.count()).select_from(AdverseEvent))).scalar() or 0
    
    enrolled = (await db.execute(select(func.count()).select_from(Participant).where(Participant.status.in_(["ENROLLED", "RANDOMIZED", "ACTIVE", "COMPLETED"])))).scalar() or 0
    total_trials = (await db.execute(select(func.count()).select_from(Trial))).scalar() or 1
    enrollment_rate = round((enrolled / max(total_participants, 1)) * 100, 1) if total_participants > 0 else 0.0
    
    kpis = {
        "active_trials": active_trials,
        "recruiting_trials": recruiting_trials,
        "total_participants": total_participants,
        "active_sites": active_sites,
        "enrollment_rate": enrollment_rate,
        "visit_compliance": visit_compliance,
        "open_data_queries": open_queries,
        "open_saes": open_saes,
        "pending_ethics": pending_ethics,
        "regulatory_items_due": reg_due,
        "total_aes": total_aes,
        "completed_visits": completed_visits,
        "overdue_visits": overdue_visits,
    }
    
    # Trial status distribution
    status_counts = {}
    statuses = ["PLANNING", "ETHICS_PENDING", "ETHICS_APPROVED", "RECRUITING", "ACTIVE", "COMPLETED", "SUSPENDED"]
    for s in statuses:
        c = (await db.execute(select(func.count()).select_from(Trial).where(Trial.status == s))).scalar() or 0
        if c > 0:
            status_counts[s] = c
    
    trial_status = {
        "labels": list(status_counts.keys()),
        "datasets": [{"data": list(status_counts.values()), "label": "Trials"}]
    }
    
    # Enrollment by site
    sites_r = await db.execute(select(Site).where(Site.status == "ACTIVE").limit(10))
    sites = sites_r.scalars().all()
    site_names = []
    site_counts = []
    for s in sites:
        pc = (await db.execute(select(func.count()).select_from(Participant).where(Participant.site_id == s.id))).scalar() or 0
        site_names.append(s.name[:20])
        site_counts.append(pc)
    
    enrollment_by_site = {
        "labels": site_names,
        "datasets": [{"data": site_counts, "label": "Enrolled"}]
    }
    
    # Participant funnel
    screened = (await db.execute(select(func.count()).select_from(Participant))).scalar() or 0
    consented = (await db.execute(select(func.count()).select_from(Participant).where(Participant.status.in_(["CONSENTED", "ENROLLED", "RANDOMIZED", "ACTIVE", "COMPLETED"])))).scalar() or 0
    randomized = (await db.execute(select(func.count()).select_from(Participant).where(Participant.status.in_(["RANDOMIZED", "ACTIVE", "COMPLETED"])))).scalar() or 0
    completed_p = (await db.execute(select(func.count()).select_from(Participant).where(Participant.status == "COMPLETED"))).scalar() or 0
    
    participant_funnel = {
        "labels": ["Screened", "Consented", "Enrolled", "Randomized", "Completed"],
        "datasets": [{"data": [screened, consented, enrolled, randomized, completed_p], "label": "Participants"}]
    }
    
    # AE severity breakdown
    ae_severity = {
        "labels": ["Mild", "Moderate", "Severe"],
        "datasets": [{"data": [
            (await db.execute(select(func.count()).select_from(AdverseEvent).where(AdverseEvent.severity == "MILD"))).scalar() or 0,
            (await db.execute(select(func.count()).select_from(AdverseEvent).where(AdverseEvent.severity == "MODERATE"))).scalar() or 0,
            (await db.execute(select(func.count()).select_from(AdverseEvent).where(AdverseEvent.severity == "SEVERE"))).scalar() or 0,
        ], "label": "AEs"}]
    }
    
    # Recent activity
    recent_r = await db.execute(select(AuditLog).order_by(AuditLog.timestamp.desc()).limit(10))
    recent = [{"action": a.action, "entity_type": a.entity_type, "user_email": a.user_email, "timestamp": str(a.timestamp), "details": a.details} for a in recent_r.scalars().all()]
    
    # Upcoming deadlines from ethics approvals
    from datetime import date
    approvals_r = await db.execute(select(EthicsApproval).where(EthicsApproval.valid_until != None).order_by(EthicsApproval.valid_until).limit(5))
    deadlines = [{"type": "Ethics Renewal", "date": str(a.valid_until), "trial_id": a.trial_id, "detail": f"Approval {a.approval_number} expires"} for a in approvals_r.scalars().all()]
    
    return {
        "kpis": kpis,
        "trial_status_distribution": trial_status,
        "enrollment_by_site": enrollment_by_site,
        "participant_funnel": participant_funnel,
        "ae_trend": ae_severity,
        "recruitment_trend": {"labels": ["Jan", "Feb", "Mar", "Apr", "May", "Jun"], "datasets": [{"data": [5, 12, 18, 25, 35, 42], "label": "Cumulative Enrollment"}]},
        "visit_compliance_data": {"labels": ["Completed", "Scheduled", "Missed", "Overdue"], "datasets": [{"data": [completed_visits, total_visits - completed_visits - overdue_visits, 0, overdue_visits], "label": "Visits"}]},
        "site_performance": enrollment_by_site,
        "recent_activity": recent,
        "upcoming_deadlines": deadlines,
    }
