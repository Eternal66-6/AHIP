from app.domain.schemas.schemas import DashboardSummary

class DashboardService:
    def get_summary(self) -> DashboardSummary:
        return DashboardSummary(
            open_cases=12,
            high_risk_cases=3,
            claim_exceptions=5,
            provider_contract_issues=2,
            compliance_gaps=1,
        )
