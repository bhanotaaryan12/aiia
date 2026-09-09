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
