from app.application.agents.patient_journey_agent import PatientJourneyAgent
from app.application.agents.claims_review_agent import ClaimsReviewAgent
from app.application.agents.provider_contract_agent import ProviderContractAgent
from app.domain.schemas.context_schemas import PatientJourneyContextPack, ClaimContextPack, ProviderContractContextPack

def test_patient_journey_agent():
    agent = PatientJourneyAgent()
    context = PatientJourneyContextPack(
        case_id="TEST_CASE",
        risk_category="High",
        journey_stage="Claim Review"
    )
    output = agent.run("TEST_CASE", context)
    assert output.agent_name == "Patient Journey Agent"
    assert output.risk_level == "High"
    assert output.next_owner == "Healthcare Operations Analyst"

def test_claims_review_agent():
    agent = ClaimsReviewAgent()
    context = ClaimContextPack(
        case_id="TEST_CASE",
        claim_status="Pended",
        amount=2000,
        cpt_codes=[]
    )
    output = agent.run("TEST_CASE", context)
    assert output.agent_name == "Claims Review Agent"
    assert output.risk_level == "High"
    assert "Missing CPT codes" in output.observation

def test_provider_contract_agent():
    agent = ProviderContractAgent()
    context = ProviderContractContextPack(
        case_id="TEST_CASE",
        network_status="Out-of-Network"
    )
    output = agent.run("TEST_CASE", context)
    assert output.agent_name == "Provider Contract Agent"
    assert output.risk_level == "High"
    assert output.next_owner == "Provider Contract Analyst"

def test_missing_context():
    agent = PatientJourneyAgent()
    context = PatientJourneyContextPack(case_id="TEST", has_error=True, error_message="Claim not found")
    output = agent.run("TEST_CASE", context)
    assert output.risk_level == "High"
    assert output.observation == "Claim not found"
