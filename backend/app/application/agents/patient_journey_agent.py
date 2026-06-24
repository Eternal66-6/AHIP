from app.application.agents.base_agent import BaseHealthcareAgent
from app.domain.schemas.schemas import AgentOutput, SharedCaseMemory
from app.domain.schemas.context_schemas import PatientJourneyContextPack

class PatientJourneyAgent(BaseHealthcareAgent):
    agent_name = "Patient Journey Agent"

    def run(self, case_id: str, context: PatientJourneyContextPack, memory: SharedCaseMemory = None) -> AgentOutput:
        if context.has_error:
            return AgentOutput(
                agent_name=self.agent_name, case_id=case_id, risk_level="High",
                observation=context.error_message or "Unknown Error", recommendation="Investigate missing data.",
                evidence=[], confidence=1.0, next_owner="System Admin"
            )

        risk_category = context.risk_category or "Standard"
        stage = context.journey_stage or "Unknown"
        
        is_high_risk = risk_category == "High"
        risk_level = "High" if is_high_risk else "Medium"
        obs = f"Patient journey is at '{stage}'. Patient risk category is '{risk_category}'."

        if memory:
            memory.observations.append(obs)
            if is_high_risk:
                memory.highest_risk_level = "High"
                memory.flags.append("HIGH_RISK_PATIENT")

        return AgentOutput(
            agent_name=self.agent_name,
            case_id=case_id,
            risk_level=risk_level,
            observation=obs,
            recommendation="Monitor claim review progress and expedite if High risk." if is_high_risk else "Standard monitoring for claim review progress.",
            evidence=[f"Journey Stage: {stage}", f"Risk Category: {risk_category}"],
            confidence=0.85,
            next_owner="Healthcare Operations Analyst" if is_high_risk else "Automated Workflow",
        )
