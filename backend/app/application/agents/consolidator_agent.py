from app.domain.schemas.schemas import SharedCaseMemory, ConsolidatedCaseOutput

class ConsolidatorAgent:
    agent_name = "Consolidator Agent"

    def run(self, case_id: str, memory: SharedCaseMemory) -> ConsolidatedCaseOutput:
        # Evaluate holistic risk based on memory
        final_risk = memory.highest_risk_level
        
        # Combine observations
        summary_obs = " | ".join(memory.observations) if memory.observations else "No observations found."
        
        # Generate consolidated recommendation
        if "OON_PROVIDER" in memory.flags:
            rec = "Escalate to Provider Contract Analyst. Case involves Out-of-Network provider."
            owner = "Provider Contract Analyst"
        elif "HIGH_RISK_CLAIM" in memory.flags:
            rec = "Escalate to Senior Claims Analyst. Claim requires manual high-risk review."
            owner = "Senior Claims Analyst"
        elif "HIGH_RISK_PATIENT" in memory.flags:
            rec = "Escalate to Healthcare Operations Analyst. High risk patient needs monitoring."
            owner = "Healthcare Operations Analyst"
        else:
            rec = "Proceed with standard automated processing. No escalations needed."
            owner = "Automated Workflow"

        return ConsolidatedCaseOutput(
            case_id=case_id,
            final_risk_level=final_risk,
            summary_observation=summary_obs,
            recommended_action=rec,
            routing_destination=owner,
            confidence_score=0.95
        )
