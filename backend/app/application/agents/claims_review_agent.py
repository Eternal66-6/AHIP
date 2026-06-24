from app.application.agents.base_agent import BaseHealthcareAgent
from app.domain.schemas.schemas import AgentOutput, SharedCaseMemory
from app.domain.schemas.context_schemas import ClaimContextPack

class ClaimsReviewAgent(BaseHealthcareAgent):
    agent_name = "Claims Review Agent"

    def run(self, case_id: str, context: ClaimContextPack, memory: SharedCaseMemory = None) -> AgentOutput:
        if context.has_error:
            return AgentOutput(
                agent_name=self.agent_name, case_id=case_id, risk_level="High",
                observation=context.error_message or "Unknown Error", recommendation="Investigate missing claim.",
                evidence=[], confidence=1.0, next_owner="System Admin"
            )

        status = context.claim_status or "Unknown"
        amount = context.amount or 0.0
        cpt_codes = context.cpt_codes

        is_pended = status == "Pended"
        missing_cpt = len(cpt_codes) == 0
        high_amount = amount > 1000
        
        # Read from memory to adjust risk
        patient_high_risk = False
        if memory and "HIGH_RISK_PATIENT" in memory.flags:
            patient_high_risk = True

        risk_level = "High" if ((is_pended and high_amount) or (is_pended and patient_high_risk)) else ("Medium" if is_pended or missing_cpt else "Low")
        
        obs = f"Claim status is {status}. Amount is ${amount}."
        if missing_cpt:
            obs += " Missing CPT codes."
        if patient_high_risk:
            obs += " Evaluated under High Risk Patient context."

        rec = "Review immediately due to high risk factors." if risk_level == "High" else "Standard claim review process."
        if missing_cpt:
            rec += " Request updated CPT codes from provider."

        if memory:
            memory.observations.append(obs)
            if risk_level == "High":
                memory.highest_risk_level = "High"
                memory.flags.append("HIGH_RISK_CLAIM")

        return AgentOutput(
            agent_name=self.agent_name,
            case_id=case_id,
            risk_level=risk_level,
            observation=obs,
            recommendation=rec,
            evidence=[f"Claim status: {status}", f"Amount: {amount}", f"CPT Codes: {cpt_codes}"],
            confidence=0.90,
            next_owner="Senior Claims Analyst" if risk_level == "High" else "Claims Analyst",
        )
