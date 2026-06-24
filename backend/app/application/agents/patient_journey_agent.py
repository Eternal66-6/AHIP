from app.application.agents.base_agent import BaseHealthcareAgent
from app.domain.schemas.schemas import AgentOutput

class PatientJourneyAgent(BaseHealthcareAgent):
    agent_name = "Patient Journey Agent"

    def run(self, case_id: str, context: dict) -> AgentOutput:
        if "error" in context:
            return AgentOutput(
                agent_name=self.agent_name, case_id=case_id, risk_level="High",
                observation=context["error"], recommendation="Investigate missing data.",
                evidence=[], confidence=1.0, next_owner="System Admin"
            )

        patient = context.get("patient", {})
        risk_category = patient.get("risk_category", "Standard")
        stage = context.get("journey_stage", "Unknown")
        
        is_high_risk = risk_category == "High"
        
        return AgentOutput(
            agent_name=self.agent_name,
            case_id=case_id,
            risk_level="High" if is_high_risk else "Medium",
            observation=f"Patient journey is at '{stage}'. Patient risk category is '{risk_category}'.",
            recommendation="Monitor claim review progress and expedite if High risk." if is_high_risk else "Standard monitoring for claim review progress.",
            evidence=[f"Journey Stage: {stage}", f"Risk Category: {risk_category}"],
            confidence=0.85,
            next_owner="Healthcare Operations Analyst" if is_high_risk else "Automated Workflow",
        )
