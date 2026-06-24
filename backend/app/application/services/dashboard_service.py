from sqlalchemy.orm import Session
from app.domain.schemas.schemas import DashboardSummary
from app.infrastructure.database.models import Claim, Patient

class DashboardService:
    def get_summary(self, db: Session) -> DashboardSummary:
        open_cases = db.query(Claim).filter(Claim.claim_status == "Pending").count()
        high_risk_cases = db.query(Patient).filter(Patient.risk_category == "High").count()
        
        return DashboardSummary(
            open_cases=open_cases,
            high_risk_cases=high_risk_cases,
            claim_exceptions=open_cases,
            provider_contract_issues=0,
            compliance_gaps=0,
        )
