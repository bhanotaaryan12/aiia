"""
AIIA CTMS Backend Generator - Part 2: Schemas & API Routes
"""
import os

BASE = r"c:\Users\nxahw\OneDrive\Desktop\proto\aiia-ctms\backend"

def w(path, content):
    fp = os.path.join(BASE, path)
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content.lstrip("\n"))

# ==============================================================
# SCHEMAS
# ==============================================================
w("app/schemas/__init__.py", "")

w("app/schemas/auth.py", '''
from pydantic import BaseModel, EmailStr
from typing import Optional, List

class LoginRequest(BaseModel):
    email: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: str
    is_active: bool
    is_superuser: bool
    roles: List[str] = []

    class Config:
        from_attributes = True

class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str
''')

w("app/schemas/user.py", '''
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    email: str
    username: str
    full_name: str
    password: str
    is_active: bool = True
    role_names: List[str] = []

class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    role_names: Optional[List[str]] = None

class UserOut(BaseModel):
    id: str
    email: str
    username: str
    full_name: str
    is_active: bool
    is_superuser: bool
    created_at: Optional[datetime] = None
    roles: List[str] = []

    class Config:
        from_attributes = True

class RoleOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    class Config:
        from_attributes = True
''')

w("app/schemas/trial.py", '''
from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class TrialCreate(BaseModel):
    title: str
    short_title: Optional[str] = None
    protocol_number: Optional[str] = None
    registration_number: Optional[str] = None
    phase: Optional[str] = None
    study_type: Optional[str] = None
    intervention_type: Optional[str] = None
    therapeutic_area: Optional[str] = None
    ayurveda_system: Optional[str] = None
    primary_objective: Optional[str] = None
    secondary_objectives: Optional[str] = None
    inclusion_criteria: Optional[str] = None
    exclusion_criteria: Optional[str] = None
    planned_sample_size: Optional[int] = None
    sponsor: Optional[str] = None
    pi_id: Optional[str] = None
    start_date: Optional[date] = None
    expected_end_date: Optional[date] = None
    status: str = "PLANNING"
    description: Optional[str] = None

class TrialUpdate(BaseModel):
    title: Optional[str] = None
    short_title: Optional[str] = None
    protocol_number: Optional[str] = None
    registration_number: Optional[str] = None
    phase: Optional[str] = None
    study_type: Optional[str] = None
    intervention_type: Optional[str] = None
    therapeutic_area: Optional[str] = None
    ayurveda_system: Optional[str] = None
    primary_objective: Optional[str] = None
    secondary_objectives: Optional[str] = None
    inclusion_criteria: Optional[str] = None
    exclusion_criteria: Optional[str] = None
    planned_sample_size: Optional[int] = None
    sponsor: Optional[str] = None
    pi_id: Optional[str] = None
    start_date: Optional[date] = None
    expected_end_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    status: Optional[str] = None
    description: Optional[str] = None

class StudyArmCreate(BaseModel):
    name: str
    description: Optional[str] = None
    allocation_ratio: float = 1.0
    arm_type: str = "TREATMENT"

class InterventionCreate(BaseModel):
    name: str
    type: Optional[str] = None
    description: Optional[str] = None
    dosage: Optional[str] = None
    duration: Optional[str] = None
    formulation: Optional[str] = None

class MilestoneCreate(BaseModel):
    name: str
    planned_date: Optional[date] = None
    status: str = "PENDING"
    notes: Optional[str] = None

class TrialOut(BaseModel):
    id: str
    title: str
    short_title: Optional[str] = None
    protocol_number: Optional[str] = None
    registration_number: Optional[str] = None
    phase: Optional[str] = None
    study_type: Optional[str] = None
    intervention_type: Optional[str] = None
    therapeutic_area: Optional[str] = None
    ayurveda_system: Optional[str] = None
    primary_objective: Optional[str] = None
    planned_sample_size: Optional[int] = None
    sponsor: Optional[str] = None
    start_date: Optional[date] = None
    expected_end_date: Optional[date] = None
    actual_end_date: Optional[date] = None
    status: Optional[str] = None
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    site_count: int = 0
    participant_count: int = 0

    class Config:
        from_attributes = True

class StudyArmOut(BaseModel):
    id: str
    name: str
    description: Optional[str] = None
    allocation_ratio: float = 1.0
    arm_type: str = "TREATMENT"
    class Config:
        from_attributes = True
''')

w("app/schemas/site.py", '''
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class SiteCreate(BaseModel):
    name: str
    institution: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: str = "India"
    pin_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    target_enrollment: Optional[int] = None

class SiteUpdate(BaseModel):
    name: Optional[str] = None
    institution: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    status: Optional[str] = None
    target_enrollment: Optional[int] = None

class SiteOut(BaseModel):
    id: str
    name: str
    institution: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    status: Optional[str] = None
    target_enrollment: Optional[int] = None
    activation_date: Optional[date] = None
    created_at: Optional[datetime] = None
    participant_count: int = 0
    class Config:
        from_attributes = True

class SiteAssignmentCreate(BaseModel):
    trial_id: str
    site_id: str
    pi_id: Optional[str] = None
    target_enrollment: Optional[int] = None

class InvestigatorCreate(BaseModel):
    site_id: str
    name: str
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    experience_years: Optional[int] = None
    gcp_trained: bool = False
    email: Optional[str] = None

class InvestigatorOut(BaseModel):
    id: str
    name: str
    site_id: str
    qualification: Optional[str] = None
    specialization: Optional[str] = None
    experience_years: Optional[int] = None
    gcp_trained: bool = False
    class Config:
        from_attributes = True
''')

w("app/schemas/participant.py", '''
from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime

class ParticipantCreate(BaseModel):
    trial_id: str
    site_id: str
    age: Optional[int] = None
    gender: Optional[str] = None

class ParticipantUpdate(BaseModel):
    status: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None

class ParticipantOut(BaseModel):
    id: str
    participant_id: str
    trial_id: str
    site_id: str
    screening_date: Optional[date] = None
    enrollment_date: Optional[date] = None
    status: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True

class ConsentCreate(BaseModel):
    participant_id: str
    consent_date: date
    consent_version: Optional[str] = None
    witness_name: Optional[str] = None

class ScreeningCreate(BaseModel):
    participant_id: str
    screening_date: date
    eligible: Optional[bool] = None
    ineligibility_reason: Optional[str] = None

class EnrollmentCreate(BaseModel):
    participant_id: str
    enrollment_date: date

class RandomizationOut(BaseModel):
    id: str
    participant_id: str
    randomization_date: Optional[date] = None
    randomization_number: Optional[str] = None
    assigned_arm_name: Optional[str] = None
    is_locked: bool = True
    class Config:
        from_attributes = True
''')

w("app/schemas/visit.py", '''
from pydantic import BaseModel
from typing import Optional
from datetime import date

class VisitDefinitionCreate(BaseModel):
    trial_id: str
    visit_name: str
    visit_number: int
    visit_type: str = "TREATMENT"
    day_offset: int = 0
    window_before: int = 3
    window_after: int = 3
    is_required: bool = True

class ParticipantVisitCreate(BaseModel):
    participant_id: str
    visit_definition_id: Optional[str] = None
    visit_name: Optional[str] = None
    scheduled_date: Optional[date] = None
    actual_date: Optional[date] = None
    status: str = "SCHEDULED"
    notes: Optional[str] = None

class ParticipantVisitUpdate(BaseModel):
    actual_date: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None

class VisitDefinitionOut(BaseModel):
    id: str
    trial_id: str
    visit_name: str
    visit_number: int
    visit_type: str
    day_offset: int = 0
    is_required: bool = True
    class Config:
        from_attributes = True

class ParticipantVisitOut(BaseModel):
    id: str
    participant_id: str
    visit_name: Optional[str] = None
    scheduled_date: Optional[date] = None
    actual_date: Optional[date] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    class Config:
        from_attributes = True
''')

w("app/schemas/form.py", '''
from pydantic import BaseModel
from typing import Optional, Any, List, Dict
from datetime import datetime

class FormCreate(BaseModel):
    trial_id: str
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    visit_type: Optional[str] = None

class FormFieldCreate(BaseModel):
    form_id: str
    field_name: str
    field_label: str
    field_type: str = "TEXT"
    is_required: bool = False
    validation_rules: Optional[Dict] = None
    options: Optional[List[str]] = None
    order_index: int = 0
    unit: Optional[str] = None
    cdisc_domain: Optional[str] = None
    cdisc_variable: Optional[str] = None

class FormSubmissionCreate(BaseModel):
    form_id: str
    participant_id: str
    visit_id: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    status: str = "DRAFT"

class FormSubmissionUpdate(BaseModel):
    data: Optional[Dict[str, Any]] = None
    status: Optional[str] = None

class DataQueryCreate(BaseModel):
    submission_id: str
    field_id: Optional[str] = None
    query_text: str
    query_type: str = "MANUAL"

class DataQueryUpdate(BaseModel):
    answer_text: Optional[str] = None
    status: Optional[str] = None

class FormOut(BaseModel):
    id: str
    trial_id: str
    name: str
    code: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    version: Optional[str] = None
    class Config:
        from_attributes = True

class FormFieldOut(BaseModel):
    id: str
    form_id: str
    field_name: str
    field_label: str
    field_type: str
    is_required: bool = False
    validation_rules: Optional[Dict] = None
    options: Optional[List[str]] = None
    order_index: int = 0
    unit: Optional[str] = None
    class Config:
        from_attributes = True

class FormSubmissionOut(BaseModel):
    id: str
    form_id: str
    participant_id: str
    submitted_at: Optional[datetime] = None
    status: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    class Config:
        from_attributes = True

class DataQueryOut(BaseModel):
    id: str
    submission_id: str
    query_text: str
    query_type: str
    status: str
    answer_text: Optional[str] = None
    class Config:
        from_attributes = True
''')

w("app/schemas/ethics.py", '''
from pydantic import BaseModel
from typing import Optional
from datetime import date

class EthicsCommitteeCreate(BaseModel):
    name: str
    institution: Optional[str] = None
    registration_number: Optional[str] = None
    chairperson: Optional[str] = None
    contact_email: Optional[str] = None

class EthicsSubmissionCreate(BaseModel):
    trial_id: str
    committee_id: Optional[str] = None
    submission_type: str = "INITIAL"
    title: Optional[str] = None
    description: Optional[str] = None

class EthicsSubmissionUpdate(BaseModel):
    status: Optional[str] = None
    submission_date: Optional[date] = None

class EthicsApprovalCreate(BaseModel):
    submission_id: str
    trial_id: str
    approval_number: Optional[str] = None
    approval_date: Optional[date] = None
    valid_from: Optional[date] = None
    valid_until: Optional[date] = None
    conditions: Optional[str] = None

class EthicsSubmissionOut(BaseModel):
    id: str
    trial_id: str
    submission_type: str
    submission_date: Optional[date] = None
    status: str
    title: Optional[str] = None
    description: Optional[str] = None
    class Config:
        from_attributes = True

class EthicsApprovalOut(BaseModel):
    id: str
    trial_id: str
    approval_number: Optional[str] = None
    approval_date: Optional[date] = None
    valid_from: Optional[date] = None
    valid_until: Optional[date] = None
    conditions: Optional[str] = None
    class Config:
        from_attributes = True

class EthicsCommitteeOut(BaseModel):
    id: str
    name: str
    institution: Optional[str] = None
    registration_number: Optional[str] = None
    class Config:
        from_attributes = True
''')

w("app/schemas/regulatory.py", '''
from pydantic import BaseModel
from typing import Optional
from datetime import date

class RegulatoryRecordCreate(BaseModel):
    trial_id: str
    record_type: str = "CTRI"
    registration_number: Optional[str] = None
    submission_date: Optional[date] = None
    status: str = "NOT_STARTED"
    notes: Optional[str] = None

class RegulatoryRecordUpdate(BaseModel):
    registration_number: Optional[str] = None
    submission_date: Optional[date] = None
    registration_date: Optional[date] = None
    status: Optional[str] = None
    last_verified_date: Optional[date] = None
    notes: Optional[str] = None

class RegulatoryChecklistCreate(BaseModel):
    trial_id: str
    category: str = "NDCT_RULES_2019"
    item_name: str
    description: Optional[str] = None

class RegulatoryChecklistUpdate(BaseModel):
    is_completed: Optional[bool] = None
    completed_date: Optional[date] = None
    notes: Optional[str] = None

class RegulatoryRecordOut(BaseModel):
    id: str
    trial_id: str
    record_type: str
    registration_number: Optional[str] = None
    submission_date: Optional[date] = None
    registration_date: Optional[date] = None
    status: str
    last_verified_date: Optional[date] = None
    notes: Optional[str] = None
    class Config:
        from_attributes = True

class RegulatoryChecklistOut(BaseModel):
    id: str
    trial_id: str
    category: str
    item_name: str
    description: Optional[str] = None
    is_completed: bool = False
    completed_date: Optional[date] = None
    notes: Optional[str] = None
    class Config:
        from_attributes = True
''')

w("app/schemas/pharmacovigilance.py", '''
from pydantic import BaseModel
from typing import Optional
from datetime import date

class AdverseEventCreate(BaseModel):
    participant_id: str
    trial_id: str
    site_id: Optional[str] = None
    event_term: str
    description: Optional[str] = None
    onset_date: Optional[date] = None
    severity: str = "MILD"
    seriousness: str = "NON_SERIOUS"
    causality: str = "POSSIBLE"
    expectedness: str = "EXPECTED"
    action_taken: Optional[str] = None
    outcome: str = "UNKNOWN"

class AdverseEventUpdate(BaseModel):
    resolution_date: Optional[date] = None
    severity: Optional[str] = None
    seriousness: Optional[str] = None
    causality: Optional[str] = None
    outcome: Optional[str] = None
    status: Optional[str] = None
    action_taken: Optional[str] = None

class SAECreate(BaseModel):
    adverse_event_id: str
    criteria: Optional[str] = None
    narrative: Optional[str] = None

class SAEUpdate(BaseModel):
    status: Optional[str] = None
    reported_to_sponsor_date: Optional[date] = None
    reported_to_ethics_date: Optional[date] = None
    reported_to_regulatory_date: Optional[date] = None
    narrative: Optional[str] = None

class CausalityAssessmentCreate(BaseModel):
    adverse_event_id: str
    method: Optional[str] = None
    causality_rating: Optional[str] = None
    rationale: Optional[str] = None

class AdverseEventOut(BaseModel):
    id: str
    participant_id: str
    trial_id: str
    event_term: str
    description: Optional[str] = None
    onset_date: Optional[date] = None
    resolution_date: Optional[date] = None
    severity: str
    seriousness: str
    causality: str
    expectedness: str
    outcome: str
    status: str
    reported_date: Optional[date] = None
    class Config:
        from_attributes = True

class SAEOut(BaseModel):
    id: str
    adverse_event_id: str
    sae_number: Optional[str] = None
    criteria: Optional[str] = None
    narrative: Optional[str] = None
    status: str
    reported_to_sponsor_date: Optional[date] = None
    reported_to_ethics_date: Optional[date] = None
    class Config:
        from_attributes = True

class SafetySignalOut(BaseModel):
    id: str
    trial_id: str
    signal_term: str
    description: Optional[str] = None
    detected_date: Optional[date] = None
    status: str
    severity: Optional[str] = None
    class Config:
        from_attributes = True
''')

w("app/schemas/document.py", '''
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class DocumentCreate(BaseModel):
    trial_id: Optional[str] = None
    title: str
    document_type: str = "OTHER"
    description: Optional[str] = None
    version: str = "1.0"

class DocumentOut(BaseModel):
    id: str
    trial_id: Optional[str] = None
    title: str
    document_type: str
    file_name: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None
    version: str = "1.0"
    status: str = "ACTIVE"
    description: Optional[str] = None
    created_at: Optional[datetime] = None
    class Config:
        from_attributes = True
''')

w("app/schemas/audit.py", '''
from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class AuditLogOut(BaseModel):
    id: str
    timestamp: Optional[datetime] = None
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    user_role: Optional[str] = None
    action: str
    entity_type: str
    entity_id: Optional[str] = None
    old_value: Optional[Any] = None
    new_value: Optional[Any] = None
    ip_address: Optional[str] = None
    details: Optional[str] = None
    class Config:
        from_attributes = True
''')

w("app/schemas/notification.py", '''
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NotificationOut(BaseModel):
    id: str
    user_id: str
    title: str
    message: Optional[str] = None
    type: str
    entity_type: Optional[str] = None
    entity_id: Optional[str] = None
    is_read: bool = False
    read_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    priority: str = "NORMAL"
    class Config:
        from_attributes = True
''')

w("app/schemas/analytics.py", '''
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class DashboardKPIs(BaseModel):
    active_trials: int = 0
    recruiting_trials: int = 0
    total_participants: int = 0
    active_sites: int = 0
    enrollment_rate: float = 0.0
    visit_compliance: float = 0.0
    open_data_queries: int = 0
    open_saes: int = 0
    pending_ethics: int = 0
    regulatory_items_due: int = 0
    total_aes: int = 0
    completed_visits: int = 0
    overdue_visits: int = 0

class ChartData(BaseModel):
    labels: List[str] = []
    datasets: List[Dict[str, Any]] = []

class DashboardData(BaseModel):
    kpis: DashboardKPIs
    recruitment_trend: ChartData
    enrollment_by_site: ChartData
    trial_status_distribution: ChartData
    ae_trend: ChartData
    participant_funnel: ChartData
    visit_compliance_data: ChartData
    site_performance: ChartData
    recent_activity: List[Dict[str, Any]] = []
    upcoming_deadlines: List[Dict[str, Any]] = []
''')

w("app/schemas/cdisc.py", '''
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class CDISCMappingOut(BaseModel):
    id: str
    internal_entity: str
    internal_field: str
    cdisc_domain: str
    cdisc_variable: str
    transformation_rule: Optional[str] = None
    is_active: bool = True
    class Config:
        from_attributes = True

class CDISCExportRequest(BaseModel):
    trial_id: str
    domains: List[str] = ["DM", "SV", "AE"]
    format: str = "csv"  # csv or json
''')

w("app/schemas/fhir.py", '''
from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class FHIRResource(BaseModel):
    resourceType: str
    id: Optional[str] = None
    meta: Optional[Dict[str, Any]] = None
    identifier: Optional[List[Dict[str, Any]]] = None

class FHIRPatient(FHIRResource):
    resourceType: str = "Patient"
    gender: Optional[str] = None
    birthDate: Optional[str] = None

class FHIRResearchStudy(FHIRResource):
    resourceType: str = "ResearchStudy"
    title: Optional[str] = None
    status: Optional[str] = None
    phase: Optional[Dict[str, Any]] = None
    description: Optional[str] = None

class FHIRResearchSubject(FHIRResource):
    resourceType: str = "ResearchSubject"
    status: Optional[str] = None
    study: Optional[Dict[str, str]] = None
    individual: Optional[Dict[str, str]] = None

class FHIRObservation(FHIRResource):
    resourceType: str = "Observation"
    status: Optional[str] = None
    code: Optional[Dict[str, Any]] = None
    valueQuantity: Optional[Dict[str, Any]] = None
    subject: Optional[Dict[str, str]] = None

class FHIRAdverseEvent(FHIRResource):
    resourceType: str = "AdverseEvent"
    actuality: str = "actual"
    event: Optional[Dict[str, Any]] = None
    subject: Optional[Dict[str, str]] = None
    date: Optional[str] = None
    seriousness: Optional[Dict[str, Any]] = None
    severity: Optional[Dict[str, Any]] = None
''')

print("Part 2 (Schemas) generated successfully.")
