from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

from app.core.config import settings
from app.core.security import get_current_user

router = APIRouter(prefix="/demo", tags=["Presentation demo"])

DEMO_RECORDS = {
    "protocol_review": {
        "title": "Protocol Review & Scientific Clearance",
        "trial_ref": "AYU-OA-2024 · Knee Osteoarthritis Efficacy Study",
        "pi_name": "Dr. Rajesh Kumar, MD (Ayu), PhD — Lead PI & Super Admin",
        "version": "Protocol Amendment v2.1 (Ethics Cleared)",
        "summary": "Formal evaluation of the scientific hypothesis, clinical trial protocol design, biomarker endpoints, and institutional governance for the multi-center Ayurveda clinical trial.",
        "status": "Ethics & Scientific Clearance Approved",
        "completion_rate": "100% Completed",
        "items": [
            {
                "label": "Scientific Hypothesis & Ayush Rationale",
                "detail": "Classical correlation of Sandhigata Vata with primary knee osteoarthritis; evaluating standardized Withania somnifera (>2.5% withanolides by HPLC) for anti-inflammatory & chondroprotective efficacy.",
                "role": "Principal Investigator",
                "priority": "HIGH",
                "tag": "Scientific Rationale",
                "status": "APPROVED",
            },
            {
                "label": "Eligibility Criteria & Exclusion Matrix",
                "detail": "Inclusion: Kellgren-Lawrence Grade II-III, age 40–70 years, baseline VAS pain score ≥40mm. Exclusion: Intra-articular steroid injections within 90 days, active rheumatoid arthritis, severe hepatic/renal impairment.",
                "role": "Trial Admin / PI",
                "priority": "CRITICAL",
                "tag": "Patient Safety",
                "status": "APPROVED",
            },
            {
                "label": "Validated Endpoints & Measurement Instruments",
                "detail": "Primary Endpoint: WOMAC pain and physical function score reduction at Week 12. Secondary Endpoints: VAS pain scale, inflammatory serum biomarkers (hs-CRP, TNF-α, IL-6), and safety biochemistry profiles.",
                "role": "Lead Biostatistician",
                "priority": "STANDARD",
                "tag": "Study Design",
                "status": "VALIDATED",
            },
            {
                "label": "Central Institutional Ethics Committee Approval",
                "detail": "Cleared by AIIA Central Institutional Ethics Committee (Registration: ECR/1382/Inst/DL/2020) under protocol approval certificate AIIA/IEC/2024/042 with zero unresolved stipulations.",
                "role": "Ethics Committee Chairperson",
                "priority": "CRITICAL",
                "tag": "Ethics Clearance",
                "status": "APPROVED",
            },
            {
                "label": "Clinical Trials Registry - India (CTRI) Registration",
                "detail": "Synchronized with national registry under CTRI Identifier CTRI/2024/03/064128; public access record validated for trial arms, interventions, and milestone dates.",
                "role": "Regulatory Officer",
                "priority": "HIGH",
                "tag": "CTRI Compliance",
                "status": "REGISTERED",
            },
            {
                "label": "Data & Safety Monitoring Board (DSMB) Charter",
                "detail": "Independent DSMB charter formally ratified; pre-specified stopping boundaries established for severe drug-induced adverse events or anomalous liver enzyme elevations.",
                "role": "DSMB Chair",
                "priority": "HIGH",
                "tag": "Safety Governance",
                "status": "RATIFIED",
            },
        ],
    },
    "operational_handoff": {
        "title": "Operational Handoff & Site Initiation",
        "trial_ref": "AYU-OA-2024 · Multi-Site Activation Phase",
        "pi_name": "Dr. Rajesh Kumar (PI) & Dr. Priya Sharma (Lead Clinical Coordinator)",
        "version": "Operational Readiness Release v1.0",
        "summary": "Governed transition from central protocol approval to distributed clinical trial operations, drug accountability, site delegation, and eCRF deployment across all 5 research centers.",
        "status": "Ready for Multi-Site Enrollment",
        "completion_rate": "100% Verified",
        "items": [
            {
                "label": "Site Initiation Visit (SIV) Completion",
                "detail": "Comprehensive Site Initiation Visits completed across all 5 study centers: AIIA Delhi (Lead Site), NIA Jaipur, IPGT&RA Jamnagar, National Institute of Siddha Chennai, and NIMHANS Bengaluru.",
                "role": "Clinical Trial Monitor",
                "priority": "CRITICAL",
                "tag": "Site Readiness",
                "status": "VERIFIED",
            },
            {
                "label": "Investigational Product (IP) Chain-of-Custody",
                "detail": "Batch #ASH-2024-009 (Ashwagandha 500mg standardized capsules) and organoleptic placebo batches received, logged, and quarantined under temperature-controlled (20–25°C) Ayurvedic pharmacy custody.",
                "role": "Unblinded Trial Pharmacist",
                "priority": "HIGH",
                "tag": "Drug Accountability",
                "status": "VERIFIED",
            },
            {
                "label": "Delegation of Authority (DOA) Log Sign-Off",
                "detail": "Comprehensive DOA log executed by Lead PI; site sub-investigators, study coordinators, phlebotomists, and data entry staff verified for certified Good Clinical Practice (GCP) credentials.",
                "role": "Principal Investigator",
                "priority": "HIGH",
                "tag": "GCP Delegation",
                "status": "SIGNED",
            },
            {
                "label": "Electronic CRF (eCRF) & EDC Deployment",
                "detail": "6 standardized CDASH-aligned electronic case report forms activated in the EDC system with automated boundary validation, required-field locks, and real-time query firing.",
                "role": "Data Manager",
                "priority": "HIGH",
                "tag": "eCRF Activation",
                "status": "DEPLOYED",
            },
            {
                "label": "Regional Language Consent Form (ICF) Distribution",
                "detail": "Patient Information Sheets and Informed Consent Forms certified and distributed in English, Hindi, Marathi, Tamil, and Kannada; audio-visual consent recording facilities calibrated.",
                "role": "Site Study Coordinator",
                "priority": "HIGH",
                "tag": "Participant Rights",
                "status": "CERTIFIED",
            },
            {
                "label": "24/7 Pharmacovigilance & SAE Emergency Channel",
                "detail": "Emergency unblinding sealed code envelopes distributed to site PIs; 24-hour expedited SAE reporting hotline and direct secure email to CDSCO and Lead PI established and tested.",
                "role": "Safety Officer / PI",
                "priority": "CRITICAL",
                "tag": "Emergency Protocol",
                "status": "OPERATIONAL",
            },
        ],
    },
    "data_safeguards": {
        "title": "Data Safeguards & Governance Architecture",
        "trial_ref": "AIIA CTMS Platform Security & Privacy Framework",
        "pi_name": "Chief Information Security & Governance Officer",
        "version": "Security & 21 CFR Part 11 Compliance Matrix",
        "summary": "Technical and operational controls ensuring complete participant confidentiality, tamper-evident audit trails, multi-tenant memory isolation, and demo environment protection.",
        "status": "Audit Verified & 100% Compliant",
        "completion_rate": "100% Enforced",
        "items": [
            {
                "label": "Dual-Key Pseudonymization Architecture",
                "detail": "Zero direct personally identifiable information (PII) stored in clinical EDC or analytical tables; participants assigned irreversible alphanumeric keys (e.g. AIIA-OA-1001) with master key stored in an air-gapped vault.",
                "role": "Data Privacy Officer",
                "priority": "CRITICAL",
                "tag": "Privacy & GDPR",
                "status": "ENFORCED",
            },
            {
                "label": "Append-Only Immutable Audit Trail (21 CFR Part 11)",
                "detail": "Every record creation, data modification, query response, and status change is immutably logged with UTC timestamp, actor ID, previous/new value delta, and IP address; delete/truncate permissions disabled.",
                "role": "Compliance Auditor",
                "priority": "CRITICAL",
                "tag": "Audit Trail",
                "status": "ACTIVE",
            },
            {
                "label": "Multi-Tenant Context Memory Isolation",
                "detail": "Graphify Knowledge Graph memory engine hashes tenant boundaries (user_<sha256>.json); strict access controls ensure investigator notes and trial memory subgraphs never cross institutional borders.",
                "role": "System Architect",
                "priority": "HIGH",
                "tag": "Graph Security",
                "status": "ISOLATED",
            },
            {
                "label": "Presentation-Only Demo Gatekeeper (RBAC)",
                "detail": "All showcase walkthrough records are locked under protected API endpoints (/api/v1/demo/*); requests from any account other than admin@aiia.gov.in receive strict HTTP 403 Forbidden responses.",
                "role": "Security Engineer",
                "priority": "HIGH",
                "tag": "API Gatekeeper",
                "status": "RESTRICTED",
            },
            {
                "label": "End-to-End Cryptographic Protection",
                "detail": "AES-256 encryption at rest across all database volumes; TLS 1.3 enforced for in-flight traffic with strict Content Security Policy (CSP) and HTTP-only JWT authentication tokens.",
                "role": "Infrastructure Lead",
                "priority": "HIGH",
                "tag": "Data Encryption",
                "status": "PROTECTED",
            },
            {
                "label": "Electronic Signatures & Database Lock Safeguards",
                "detail": "Database freeze protocol prevents retrospective edits post-interim analysis; unblinding and dataset unlocking requires dual cryptographic sign-offs from both the Lead PI and Senior Biostatistician.",
                "role": "Lead PI & Biostatistician",
                "priority": "CRITICAL",
                "tag": "Data Lock",
                "status": "LOCKED",
            },
        ],
    },
    "clinical_monitoring": {
        "title": "Clinical Site Monitoring & Source Data Verification",
        "trial_ref": "AYU-OA-2024 · Quality Assurance Visit Report",
        "pi_name": "Dr. Rajesh Kumar (Lead PI) & Lead Clinical Monitor",
        "version": "Routine Monitoring Cycle 1 (Q2 2024)",
        "summary": "Simulated monitoring visit findings, source data verification (SDV) coverage, and GCP adherence tracking across active study sites.",
        "status": "Monitoring Cycle 1 Passed",
        "completion_rate": "100% SDV on Target Cohort",
        "items": [
            {
                "label": "Source Data Verification (SDV) Coverage",
                "detail": "Completed 100% SDV for the initial cohort of 30 randomized subjects at AIIA Delhi; primary efficacy measures (WOMAC) and safety lab reports cross-verified against site medical records.",
                "role": "Clinical Research Associate",
                "priority": "CRITICAL",
                "tag": "SDV Audit",
                "status": "VERIFIED",
            },
            {
                "label": "Investigational Product Reconciliation",
                "detail": "Full accountability reconciliation between dispensed capsules and returned blister packs; subject adherence calculated at 94.8% with zero dosage diversion identified.",
                "role": "Site Study Pharmacist",
                "priority": "HIGH",
                "tag": "IP Adherence",
                "status": "RECONCILED",
            },
            {
                "label": "Protocol Deviation Surveillance",
                "detail": "Zero major protocol deviations recorded; 2 minor administrative visit window deviations (+2 days due to public holidays) reviewed, logged, and cleared by PI.",
                "role": "Lead PI",
                "priority": "STANDARD",
                "tag": "Protocol Compliance",
                "status": "CLEARED",
            },
        ],
    },
    "safety_surveillance": {
        "title": "Pharmacovigilance & Safety Signal Surveillance",
        "trial_ref": "AYU-OA-2024 & AYU-DM-2024 Cross-Trial Safety Board",
        "pi_name": "Dr. Rajesh Kumar (PI) & Dr. Anita Verma (Pharmacovigilance Officer)",
        "version": "Monthly Safety Surveillance Summary",
        "summary": "Real-time pharmacovigilance surveillance, expedited 24-hour SAE escalation tracking to regulatory bodies, and signal clustering evaluation.",
        "status": "Surveillance Active — Zero Uncontrolled Signals",
        "completion_rate": "100% Compliance",
        "items": [
            {
                "label": "24-Hour Expedited SAE Escalation Workflow",
                "detail": "Verified automated notification pipelines to CDSCO, Central Ethics Committee, and Trial Sponsor within mandated 24-hour statutory reporting timelines.",
                "role": "Pharmacovigilance Officer",
                "priority": "CRITICAL",
                "tag": "Expedited Reporting",
                "status": "OPERATIONAL",
            },
            {
                "label": "Automated Signal Detection & MedDRA Clustering",
                "detail": "Continuous background clustering of adverse event terms shows standard mild GI upset (3.2%) with zero unexpected organ toxicities or safety signal thresholds crossed.",
                "role": "Safety Biostatistician",
                "priority": "HIGH",
                "tag": "Signal Detection",
                "status": "CLEAR",
            },
            {
                "label": "DSMB Interim Safety Milestone Review",
                "detail": "Data and Safety Monitoring Board convened for 50% enrollment milestone; recommendation issued to proceed without protocol modification or dosing adjustment.",
                "role": "DSMB Chairperson",
                "priority": "HIGH",
                "tag": "Interim Review",
                "status": "ENDORSED",
            },
        ],
    },
    "cdisc_standards_validation": {
        "title": "CDISC SDTM & Regulatory Submission Package",
        "trial_ref": "AYU-OA-2024 · Submission Readiness Bundle",
        "pi_name": "Dr. Rajesh Kumar (PI) & Data Management Lead",
        "version": "SDTM Implementation Guide v3.3 Compliant",
        "summary": "Standardized Clinical Data Interchange Standards Consortium (CDISC) SDTM datasets generated directly from eCRF submissions for regulatory authority filing.",
        "status": "Validated for CTRI & CDSCO Dossier",
        "completion_rate": "Validated Domains: DM, SV, AE",
        "items": [
            {
                "label": "Demographics (DM) Domain Conformance",
                "detail": "All 60 enrolled participants mapped to SDTM DM variables (SUBJID, AGE, SEX, RACE, ARMCD, ARM, RFSTDTC) with automated Pinnacle 21 rule validation.",
                "role": "CDISC Standards Specialist",
                "priority": "HIGH",
                "tag": "SDTM DM",
                "status": "COMPLIANT",
            },
            {
                "label": "Subject Visits (SV) Schedule Conformance",
                "detail": "385 completed participant visits mapped to SV domain (VISITNUM, VISIT, SVDTC, SVSTDTC, SVENDTC) demonstrating 80.9% on-schedule protocol adherence.",
                "role": "Statistical Programmer",
                "priority": "HIGH",
                "tag": "SDTM SV",
                "status": "COMPLIANT",
            },
            {
                "label": "Adverse Events (AE) MedDRA Coding Conformance",
                "detail": "All 25 reported adverse events coded with MedDRA dictionary hierarchy (System Organ Class, Preferred Term) and CTCAE severity grading for automated export.",
                "role": "Medical Coder",
                "priority": "HIGH",
                "tag": "SDTM AE",
                "status": "COMPLIANT",
            },
        ],
    },
}


class ChecklistToggle(BaseModel):
    item_label: str
    completed: bool


@router.get("/records")
async def get_demo_records(current_user=Depends(get_current_user)):
    if current_user.email.lower() != settings.DEMO_ACCOUNT_EMAIL.lower():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Demo records are restricted to the presentation account")
    return {"records": DEMO_RECORDS}


@router.get("/records/{record_key}")
async def get_demo_record(record_key: str, current_user=Depends(get_current_user)):
    if current_user.email.lower() != settings.DEMO_ACCOUNT_EMAIL.lower():
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Demo records are restricted to the presentation account")
    if record_key not in DEMO_RECORDS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return {"record": DEMO_RECORDS[record_key]}
