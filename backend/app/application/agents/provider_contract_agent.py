from app.application.agents.base_agent import BaseHealthcareAgent
from app.domain.schemas.schemas import AgentOutput

class ProviderContractAgent(BaseHealthcareAgent):
    agent_name = "Provider Contract Agent"

    def run(self, case_id: str, context: dict) -> AgentOutput:
        if "error" in context:
            return AgentOutput(
                agent_name=self.agent_name, case_id=case_id, risk_level="High",
                observation=context["error"], recommendation="Investigate missing claim context.",
                evidence=[], confidence=1.0, next_owner="System Admin"
            )

        provider = context.get("provider", {})
        network_status = provider.get("network_status", "Unknown")
        
        is_oon = network_status == "Out-of-Network"

        return AgentOutput(
            agent_name=self.agent_name,
            case_id=case_id,
            risk_level="High" if is_oon else "Low",
            observation=f"Provider network status is '{network_status}'.",
            recommendation="Assign to Provider Contract Analyst to negotiate single case agreement or review out-of-network benefits." if is_oon else "Contract is active and In-Network. No action needed.",
            evidence=[f"Network Status: {network_status}", f"Provider ID: {provider.get('provider_id')}"],
            confidence=0.95,
            next_owner="Provider Contract Analyst" if is_oon else "Automated Workflow",
        )
