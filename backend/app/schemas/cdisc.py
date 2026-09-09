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
