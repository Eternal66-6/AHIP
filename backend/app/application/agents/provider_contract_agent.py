from app.application.agents.base_agent import BaseHealthcareAgent
from app.domain.schemas.schemas import AgentOutput, SharedCaseMemory
from app.domain.schemas.context_schemas import ProviderContractContextPack

class ProviderContractAgent(BaseHealthcareAgent):
    agent_name = "Provider Contract Agent"

    def run(self, case_id: str, context: ProviderContractContextPack, memory: SharedCaseMemory = None) -> AgentOutput:
        if context.has_error:
            return AgentOutput(
                agent_name=self.agent_name, case_id=case_id, risk_level="High",
                observation=context.error_message or "Unknown Error", recommendation="Investigate missing claim context.",
                evidence=[], confidence=1.0, next_owner="System Admin"
            )

        network_status = context.network_status or "Unknown"
        is_oon = network_status == "Out-of-Network"
        
        risk_level = "High" if is_oon else "Low"
        obs = f"Provider network status is '{network_status}'."
        
        if memory:
            memory.observations.append(obs)
            if risk_level == "High":
                memory.highest_risk_level = "High"
                memory.flags.append("OON_PROVIDER")

        return AgentOutput(
            agent_name=self.agent_name,
            case_id=case_id,
            risk_level=risk_level,
            observation=obs,
            recommendation="Assign to Provider Contract Analyst to negotiate single case agreement or review out-of-network benefits." if is_oon else "Contract is active and In-Network. No action needed.",
            evidence=[f"Network Status: {network_status}", f"Provider ID: {context.provider_id}"],
            confidence=0.95,
            next_owner="Provider Contract Analyst" if is_oon else "Automated Workflow",
        )
