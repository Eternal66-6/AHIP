export type DashboardSummary = {
  open_cases: number
  high_risk_cases: number
  claim_exceptions: number
  provider_contract_issues: number
  compliance_gaps: number
}

export type Patient = {
  patient_id: string
  name: string
  plan_id: string
  status: string
  risk_category: string
}

export type Claim = {
  claim_id: string
  patient_id: string
  provider_id: string
  service_date: string
  claim_status: string
  amount: number
}

export type Provider = {
  provider_id: string
  name: string
  type: string
  network_status: string
}
