from pydantic import BaseModel
from typing import List, Optional

class ClaimContextPack(BaseModel):
    case_id: str
    claim_id: Optional[str] = None
    claim_status: Optional[str] = None
    amount: Optional[float] = None
    cpt_codes: List[str] = []
    icd_codes: List[str] = []
    has_error: bool = False
    error_message: Optional[str] = None

class PatientJourneyContextPack(BaseModel):
    case_id: str
    member_id: Optional[str] = None
    patient_status: Optional[str] = None
    risk_category: Optional[str] = None
    journey_stage: Optional[str] = None
    recent_events: List[str] = []
    has_error: bool = False
    error_message: Optional[str] = None

class ProviderContractContextPack(BaseModel):
    case_id: str
    provider_id: Optional[str] = None
    provider_type: Optional[str] = None
    network_status: Optional[str] = None
    has_error: bool = False
    error_message: Optional[str] = None

class ComplianceContextPack(BaseModel):
    case_id: str
    claim_id: Optional[str] = None
    cpt_codes: List[str] = []
    icd_codes: List[str] = []
    missing_documentation_risk: bool = False
    audit_required: bool = False
    has_error: bool = False
    error_message: Optional[str] = None
