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
