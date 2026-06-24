from sqlalchemy.orm import Session
from datetime import datetime
from app.application.context.context_builder import HealthcareContextBuilder
from app.application.agents.claims_review_agent import ClaimsReviewAgent
from app.application.agents.provider_contract_agent import ProviderContractAgent
from app.application.agents.patient_journey_agent import PatientJourneyAgent
from app.infrastructure.database.models import AgentExecutionLog

class WorkflowOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.context_builder = HealthcareContextBuilder(db)

    def run_case_review(self, case_id: str) -> dict:
        agent_outputs = [
            PatientJourneyAgent().run(case_id, self.context_builder.build_patient_journey_context(case_id)),
            ClaimsReviewAgent().run(case_id, self.context_builder.build_claim_context(case_id)),
            ProviderContractAgent().run(case_id, self.context_builder.build_provider_contract_context(case_id)),
        ]
        
        # Save to DB (Agent Memory)
        now = datetime.utcnow().isoformat()
        for output in agent_outputs:
            log = AgentExecutionLog(
                case_id=output.case_id,
                agent_name=output.agent_name,
                input_summary="Context loaded from DB",
                observation=output.observation,
                recommendation=output.recommendation,
                confidence=output.confidence,
                related_workflow_event=None,
                created_at=now
            )
            self.db.add(log)
        
        self.db.commit()

        return {
            "case_id": case_id,
            "agent_outputs": [o.model_dump() for o in agent_outputs],
            "summary": "Phase 2 multi-agent review completed and logged to memory."
        }
