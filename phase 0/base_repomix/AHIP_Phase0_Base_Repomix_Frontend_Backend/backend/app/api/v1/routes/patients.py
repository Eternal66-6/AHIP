from fastapi import APIRouter
router = APIRouter()

@router.get("/")
def list_patients():
    return [{"member_id": "MEM-001", "name": "Demo Patient One", "plan_id": "PLAN-GOLD", "status": "Active"}]
