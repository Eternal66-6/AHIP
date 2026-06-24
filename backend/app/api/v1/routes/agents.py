from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.infrastructure.database.session import get_db
from app.infrastructure.database.models import AgentExecutionLog
from app.domain.schemas.schemas import AgentRunRequest
from app.application.agents.orchestrator import WorkflowOrchestrator

router = APIRouter()

@router.post("/run-case-review")
def run_case_review(request: AgentRunRequest, db: Session = Depends(get_db)):
    return WorkflowOrchestrator(db).run_case_review(request.case_id)

@router.get("/logs")
def get_agent_logs(db: Session = Depends(get_db)):
    logs = db.query(AgentExecutionLog).order_by(AgentExecutionLog.created_at.desc()).all()
    return [
        {
            "id": log.id,
            "case_id": log.case_id,
            "agent_name": log.agent_name,
            "observation": log.observation,
            "recommendation": log.recommendation,
            "confidence": log.confidence,
            "created_at": log.created_at
        }
        for log in logs
    ]

from app.application.context.context_builder import HealthcareContextBuilder

@router.get("/context/{case_id}")
def get_case_context_mapping(case_id: str, db: Session = Depends(get_db)):
    builder = HealthcareContextBuilder(db)
    return {
        "case_id": case_id,
        "patient_journey": builder.build_patient_journey_context(case_id).model_dump(),
        "claim": builder.build_claim_context(case_id).model_dump(),
        "provider_contract": builder.build_provider_contract_context(case_id).model_dump(),
        "compliance": builder.build_compliance_context(case_id).model_dump(),
    }
