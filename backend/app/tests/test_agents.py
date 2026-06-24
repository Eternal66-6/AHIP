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

from app.domain.schemas.schemas import SharedCaseMemory
from app.application.agents.consolidator_agent import ConsolidatorAgent

def test_collaboration_pipeline():
    memory = SharedCaseMemory(case_id="COLLAB_TEST")
    
    # 1. Patient Agent adds High Risk Flag
    pj_agent = PatientJourneyAgent()
    pj_context = PatientJourneyContextPack(case_id="COLLAB_TEST", risk_category="High", journey_stage="Claim Review")
    pj_agent.run("COLLAB_TEST", pj_context, memory)
    
    assert "HIGH_RISK_PATIENT" in memory.flags
    assert memory.highest_risk_level == "High"

    # 2. Claims Agent reads High Risk Flag
    cr_agent = ClaimsReviewAgent()
    cr_context = ClaimContextPack(case_id="COLLAB_TEST", claim_status="Pended", amount=200, cpt_codes=["99213"])
    cr_output = cr_agent.run("COLLAB_TEST", cr_context, memory)
    
    # Even though amount is low, patient is high risk, so claim is high risk
    assert cr_output.risk_level == "High"
    assert "Evaluated under High Risk Patient context" in cr_output.observation
    
    # 3. Consolidator reads memory
    cons_agent = ConsolidatorAgent()
    cons_output = cons_agent.run("COLLAB_TEST", memory)
    
    assert cons_output.final_risk_level == "High"
    assert "High risk patient" in cons_output.recommended_action
