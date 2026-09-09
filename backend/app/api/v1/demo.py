from fastapi import APIRouter, Depends, HTTPException, status

from app.core.config import settings
from app.core.security import get_current_user

router = APIRouter(prefix="/demo", tags=["Presentation demo"])

DEMO_RECORDS = {
    "protocol_review": {
        "title": "Protocol review",
        "summary": "A guided protocol-readiness conversation for the presentation.",
        "status": "Ready for walkthrough",
        "items": [
            {"label": "Study purpose", "detail": "Explain the research question and intended governance scope."},
            {"label": "Responsible roles", "detail": "Identify the investigator, coordinator, and review responsibilities."},
            {"label": "Approval pathway", "detail": "Discuss how protocol and ethics review would be documented in production."},
        ],
    },
    "operational_handoff": {
        "title": "Operational handoff",
        "summary": "A simplified handoff from setup to site coordination.",
        "status": "Ready for walkthrough",
        "items": [
            {"label": "Prepare study workspace", "detail": "Confirm the study workspace and role assignments before handoff."},
            {"label": "Brief the site team", "detail": "Use the presentation record to explain what the site would receive."},
            {"label": "Record review points", "detail": "Demonstrate where implementation notes would be captured in a production build."},
        ],
    },
    "data_safeguards": {
        "title": "Data safeguards",
        "summary": "The demonstration boundaries and protections that keep the prototype safe to present.",
        "status": "Presentation-safe",
        "items": [
            {"label": "No patient information", "detail": "The demo contains illustrative content only and must not receive patient data."},
            {"label": "Demo-account restriction", "detail": "Example walkthrough records are only available to the designated demo account."},
            {"label": "Secure production path", "detail": "Production use requires organisation-approved identity, hosting, retention, and review controls."},
        ],
    },
    "clinical_monitoring": {
        "title": "Clinical site monitoring & compliance",
        "summary": "Simulated routine monitoring visit findings and source data verification status for the demo account.",
        "status": "Ready for walkthrough",
        "items": [
            {"label": "Source Data Verification (SDV)", "detail": "Completed 100% SDV for initial cohort of 30 consented subjects at AIIA Delhi."},
            {"label": "Investigational Product Reconciliation", "detail": "Ashwagandha churna and placebo batch accountability confirmed with zero discrepancies."},
            {"label": "Protocol Adherence Verification", "detail": "All inclusion/exclusion criteria verified; zero major protocol deviations logged."},
        ],
    },
    "safety_surveillance": {
        "title": "Pharmacovigilance & safety walkthrough",
        "summary": "Illustrative safety tracking and signal surveillance metrics for the demo session.",
        "status": "Ready for walkthrough",
        "items": [
            {"label": "Expedited Reporting Protocol", "detail": "Verified 24-hour SAE escalation workflow to CDSCO and Central Ethics Committee."},
            {"label": "Signal Detection Review", "detail": "Automated clustering algorithm shows no adverse signal spikes across active trial arms."},
            {"label": "DSMB Interim Evaluation", "detail": "Data and Safety Monitoring Board scheduled for Q3 interim efficacy analysis."},
        ],
    },
    "cdisc_standards_validation": {
        "title": "CDISC SDTM & regulatory export",
        "summary": "Sample regulatory export mapping data for DM, AE, and SV domains prepared for CTRI submission.",
        "status": "Ready for walkthrough",
        "items": [
            {"label": "Demographics (DM) Domain", "detail": "Standardized mapping of age, gender, and randomized treatment arms validated."},
            {"label": "Subject Visits (SV) Domain", "detail": "Scheduled visit compliance tracking aligned with protocol timepoints."},
            {"label": "Adverse Events (AE) Domain", "detail": "MedDRA coding compatibility and CTCAE severity grading verified."},
        ],
    },
}


@router.get("/records")
async def get_demo_records(current_user=Depends(get_current_user)):
    if current_user.email.lower() != settings.DEMO_ACCOUNT_EMAIL.lower():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Demo records are restricted to the presentation account")
    return {"records": DEMO_RECORDS}
