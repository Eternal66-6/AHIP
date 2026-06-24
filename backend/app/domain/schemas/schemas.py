from pydantic import BaseModel
from datetime import date

class PatientBase(BaseModel):
    member_id: str
    name: str
    plan_id: str
    status: str
    risk_category: str

class Patient(PatientBase):
    id: int
    class Config:
        from_attributes = True

class ProviderBase(BaseModel):
    provider_id: str
    name: str
    type: str
    network_status: str

class Provider(ProviderBase):
    id: int
    class Config:
        from_attributes = True

class ClaimBase(BaseModel):
    claim_id: str
    patient_member_id: str
    provider_id: str
    service_date: date
    claim_status: str
    amount: int
    cpt_codes: list[str]
    icd_codes: list[str]

class Claim(ClaimBase):
    id: int
    class Config:
        from_attributes = True

class AgentRunRequest(BaseModel):
    case_id: str

class AgentOutput(BaseModel):
    agent_name: str
    case_id: str
    risk_level: str
    observation: str
    recommendation: str
    evidence: list[str]
    confidence: float
    next_owner: str | None = None

class DashboardSummary(BaseModel):
    open_cases: int
    high_risk_cases: int
    claim_exceptions: int
    provider_contract_issues: int
    compliance_gaps: int

class SharedCaseMemory(BaseModel):
    case_id: str
    observations: list[str] = []
    highest_risk_level: str = "Low"
    flags: list[str] = []

class ConsolidatedCaseOutput(BaseModel):
    case_id: str
    final_risk_level: str
    summary_observation: str
    recommended_action: str
    routing_destination: str
    confidence_score: float

class DecisionRequest(BaseModel):
    action: str  # "Accept" or "Override"
