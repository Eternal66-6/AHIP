# AHIP Phase 1 - API Endpoints

The FastAPI backend exposes the following REST endpoints to interact with the healthcare data models.

## Dashboard Summary
`GET /api/v1/dashboard/summary`
Calculates dynamic totals by querying the database.
- **Returns**: `DashboardSummary`
```json
{
  "open_cases": 1,
  "high_risk_cases": 1,
  "claim_exceptions": 1,
  "provider_contract_issues": 0,
  "compliance_gaps": 0
}
```

## Patients
`GET /api/v1/patients/`
- **Returns**: Array of Patient objects.

`GET /api/v1/patients/{patient_id}`
- **Returns**: Single Patient object or 404.

`POST /api/v1/patients/`
- **Body**: `PatientBase`
- **Returns**: Created Patient object.

## Providers
`GET /api/v1/providers/`
- **Returns**: Array of Provider objects.

`GET /api/v1/providers/{provider_id}`
- **Returns**: Single Provider object or 404.

`POST /api/v1/providers/`
- **Body**: `ProviderBase`
- **Returns**: Created Provider object.

## Claims
`GET /api/v1/claims/`
- **Returns**: Array of Claim objects.

`GET /api/v1/claims/{claim_id}`
- **Returns**: Single Claim object or 404.

`POST /api/v1/claims/`
- **Body**: `ClaimBase`
- **Returns**: Created Claim object.
