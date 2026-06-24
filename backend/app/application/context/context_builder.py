from sqlalchemy.orm import Session
from app.infrastructure.database.models import Claim, Patient, Provider
from app.domain.schemas.context_schemas import (
    ClaimContextPack, 
    PatientJourneyContextPack, 
    ProviderContractContextPack, 
    ComplianceContextPack
)

class HealthcareContextBuilder:
    def __init__(self, db: Session):
        self.db = db

    def _get_claim_and_relations(self, case_id: str):
        claim = self.db.query(Claim).filter(Claim.claim_id == case_id).first()
        return claim

    def build_claim_context(self, case_id: str) -> ClaimContextPack:
        claim = self._get_claim_and_relations(case_id)
        if not claim:
            return ClaimContextPack(case_id=case_id, has_error=True, error_message="Claim not found")
        
        return ClaimContextPack(
            case_id=case_id,
            claim_id=claim.claim_id,
            claim_status=claim.claim_status,
            amount=claim.amount,
            cpt_codes=claim.cpt_codes or [],
            icd_codes=claim.icd_codes or []
        )

    def build_patient_journey_context(self, case_id: str) -> PatientJourneyContextPack:
        claim = self._get_claim_and_relations(case_id)
        if not claim:
            return PatientJourneyContextPack(case_id=case_id, has_error=True, error_message="Claim not found")
        
        patient = claim.patient
        return PatientJourneyContextPack(
            case_id=case_id,
            member_id=patient.member_id if patient else None,
            patient_status=patient.status if patient else None,
            risk_category=patient.risk_category if patient else None,
            journey_stage="Claim Review",
            recent_events=[f"CLAIM_{claim.claim_status.upper()}"]
        )

    def build_provider_contract_context(self, case_id: str) -> ProviderContractContextPack:
        claim = self._get_claim_and_relations(case_id)
        if not claim:
            return ProviderContractContextPack(case_id=case_id, has_error=True, error_message="Claim not found")
        
        provider = claim.provider
        return ProviderContractContextPack(
            case_id=case_id,
            provider_id=provider.provider_id if provider else None,
            provider_type=provider.type if provider else None,
            network_status=provider.network_status if provider else None
        )
        
    def build_compliance_context(self, case_id: str) -> ComplianceContextPack:
        claim = self._get_claim_and_relations(case_id)
        if not claim:
            return ComplianceContextPack(case_id=case_id, has_error=True, error_message="Claim not found")
            
        cpt = claim.cpt_codes or []
        icd = claim.icd_codes or []
        missing_doc = len(cpt) == 0 or len(icd) == 0
        
        return ComplianceContextPack(
            case_id=case_id,
            claim_id=claim.claim_id,
            cpt_codes=cpt,
            icd_codes=icd,
            missing_documentation_risk=missing_doc,
            audit_required=missing_doc and claim.amount and claim.amount > 1000
        )
