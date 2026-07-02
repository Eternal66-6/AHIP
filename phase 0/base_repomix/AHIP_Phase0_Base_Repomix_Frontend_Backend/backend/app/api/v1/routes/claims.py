from fastapi import APIRouter
router = APIRouter()

@router.get("/")
def list_claims():
    return [{"claim_id": "CLM-001", "patient_member_id": "MEM-001", "provider_id": "PROV-001", "claim_status": "Pended", "amount": 1250}]
