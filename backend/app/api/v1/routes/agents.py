from fastapi import APIRouter
from app.domain.schemas.schemas import AgentRunRequest
from app.application.agents.orchestrator import WorkflowOrchestrator

router = APIRouter()

@router.post("/run-case-review")
def run_case_review(request: AgentRunRequest):
    return WorkflowOrchestrator().run_case_review(request.case_id)
