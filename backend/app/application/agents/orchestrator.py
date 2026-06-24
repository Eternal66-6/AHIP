from sqlalchemy.orm import Session
from datetime import datetime
from app.application.context.context_builder import HealthcareContextBuilder
from app.application.agents.claims_review_agent import ClaimsReviewAgent
from app.application.agents.provider_contract_agent import ProviderContractAgent
from app.application.agents.patient_journey_agent import PatientJourneyAgent
from app.application.agents.consolidator_agent import ConsolidatorAgent
from app.infrastructure.database.models import AgentExecutionLog
from app.domain.schemas.schemas import SharedCaseMemory

class WorkflowOrchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.context_builder = HealthcareContextBuilder(db)

    def run_case_review(self, case_id: str) -> dict:
        memory = SharedCaseMemory(case_id=case_id)
        
        # Pipeline Execution (Handoff Protocol)
        pj_output = PatientJourneyAgent().run(case_id, self.context_builder.build_patient_journey_context(case_id), memory)
        cr_output = ClaimsReviewAgent().run(case_id, self.context_builder.build_claim_context(case_id), memory)
        pc_output = ProviderContractAgent().run(case_id, self.context_builder.build_provider_contract_context(case_id), memory)
        
        agent_outputs = [pj_output, cr_output, pc_output]
        
        # Consolidation Phase
        consolidated_output = ConsolidatorAgent().run(case_id, memory)
        
        # Save to DB (Agent Memory)
        now = datetime.utcnow().isoformat()
        for output in agent_outputs:
            log = AgentExecutionLog(
                case_id=output.case_id,
                agent_name=output.agent_name,
                input_summary="Context loaded from DB with Shared Memory",
                observation=output.observation,
                recommendation=output.recommendation,
                confidence=output.confidence,
                related_workflow_event=None,
                created_at=now
            )
            self.db.add(log)
            
        # Log Consolidated Output
        cons_log = AgentExecutionLog(
            case_id=consolidated_output.case_id,
            agent_name="Consolidator Agent",
            input_summary="Processed SharedCaseMemory",
            observation=consolidated_output.summary_observation,
            recommendation=consolidated_output.recommended_action,
            confidence=consolidated_output.confidence_score,
            related_workflow_event=consolidated_output.routing_destination,
            created_at=now
        )
        self.db.add(cons_log)
        self.db.commit()

        return {
            "case_id": case_id,
            "agent_outputs": [o.model_dump() for o in agent_outputs],
            "consolidated_output": consolidated_output.model_dump(),
            "shared_memory_flags": memory.flags,
            "summary": "Phase 4 collaborative multi-agent pipeline completed."
        }
