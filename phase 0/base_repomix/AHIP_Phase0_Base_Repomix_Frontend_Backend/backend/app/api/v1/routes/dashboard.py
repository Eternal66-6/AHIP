from fastapi import APIRouter
from app.application.services.dashboard_service import DashboardService

router = APIRouter()

@router.get("/summary")
def dashboard_summary():
    return DashboardService().get_summary()
