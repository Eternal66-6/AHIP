from pydantic import BaseModel

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
