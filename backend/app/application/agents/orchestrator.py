from app.application.context.context_builder import HealthcareContextBuilder
from app.application.agents.claims_review_agent import ClaimsReviewAgent
from app.application.agents.provider_contract_agent import ProviderContractAgent
from app.application.agents.patient_journey_agent import PatientJourneyAgent

class WorkflowOrchestrator:
    def __init__(self):
        self.context_builder = HealthcareContextBuilder()

    def run_case_review(self, case_id: str) -> dict:
        outputs = [
            PatientJourneyAgent().run(case_id, self.context_builder.build_patient_journey_context(case_id)).model_dump(),
            ClaimsReviewAgent().run(case_id, self.context_builder.build_claim_context(case_id)).model_dump(),
            ProviderContractAgent().run(case_id, self.context_builder.build_provider_contract_context(case_id)).model_dump(),
        ]
        return {
            "case_id": case_id,
            "agent_outputs": outputs,
            "summary": "Phase 0 sample multi-agent review completed."
        }
