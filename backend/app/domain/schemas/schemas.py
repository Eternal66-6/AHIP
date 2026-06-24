from pydantic import BaseModel
from datetime import date

class PatientBase(BaseModel):
    patient_id: str
    name: str
    plan_id: str
    status: str
    risk_category: str

class Patient(PatientBase):
    class Config:
        orm_mode = True

class ProviderBase(BaseModel):
    provider_id: str
    name: str
    type: str
    network_status: str

class Provider(ProviderBase):
    class Config:
        orm_mode = True

class ClaimBase(BaseModel):
    claim_id: str
    patient_id: str
    provider_id: str
    service_date: date
    claim_status: str
    amount: float

class Claim(ClaimBase):
    class Config:
        orm_mode = True

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
