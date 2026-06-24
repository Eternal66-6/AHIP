from sqlalchemy.orm import Session
from app.infrastructure.database.models import Claim, Patient, Provider

class HealthcareContextBuilder:
    def __init__(self, db: Session):
        self.db = db

    def _get_base_context(self, case_id: str) -> dict:
        claim = self.db.query(Claim).filter(Claim.claim_id == case_id).first()
        if not claim:
            return {"case_id": case_id, "error": "Claim not found"}
        
        patient = claim.patient
        provider = claim.provider

        return {
            "case_id": case_id,
            "claim": {
                "claim_status": claim.claim_status,
                "amount": claim.amount,
                "cpt_codes": claim.cpt_codes or [],
                "icd_codes": claim.icd_codes or []
            },
            "patient": {
                "member_id": patient.member_id if patient else None,
                "status": patient.status if patient else None,
                "risk_category": patient.risk_category if patient else None,
            },
            "provider": {
                "provider_id": provider.provider_id if provider else None,
                "network_status": provider.network_status if provider else None,
                "type": provider.type if provider else None
            }
        }

    def build_claim_context(self, case_id: str) -> dict:
        return self._get_base_context(case_id)

    def build_patient_journey_context(self, case_id: str) -> dict:
        base = self._get_base_context(case_id)
        if "error" in base:
            return base
            
        base["journey_stage"] = "Claim Review"
        base["events"] = [f"CLAIM_{base['claim']['claim_status'].upper()}"]
        return base

    def build_provider_contract_context(self, case_id: str) -> dict:
        return self._get_base_context(case_id)
