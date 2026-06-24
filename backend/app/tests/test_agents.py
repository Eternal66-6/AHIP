from app.application.agents.patient_journey_agent import PatientJourneyAgent
from app.application.agents.claims_review_agent import ClaimsReviewAgent
from app.application.agents.provider_contract_agent import ProviderContractAgent

def test_patient_journey_agent():
    agent = PatientJourneyAgent()
    context = {
        "patient": {"risk_category": "High"},
        "journey_stage": "Claim Review",
    }
    output = agent.run("TEST_CASE", context)
    assert output.agent_name == "Patient Journey Agent"
    assert output.risk_level == "High"
    assert output.next_owner == "Healthcare Operations Analyst"

def test_claims_review_agent():
    agent = ClaimsReviewAgent()
    context = {
        "claim": {
            "claim_status": "Pended",
            "amount": 2000,
            "cpt_codes": []
        }
    }
    output = agent.run("TEST_CASE", context)
    assert output.agent_name == "Claims Review Agent"
    assert output.risk_level == "High"
    assert "Missing CPT codes" in output.observation

def test_provider_contract_agent():
    agent = ProviderContractAgent()
    context = {
        "provider": {
            "network_status": "Out-of-Network"
        }
    }
    output = agent.run("TEST_CASE", context)
    assert output.agent_name == "Provider Contract Agent"
    assert output.risk_level == "High"
    assert output.next_owner == "Provider Contract Analyst"

def test_missing_context():
    agent = PatientJourneyAgent()
    output = agent.run("TEST_CASE", {"error": "Claim not found"})
    assert output.risk_level == "High"
    assert output.observation == "Claim not found"
