export type DashboardSummary = {
  open_cases: number
  high_risk_cases: number
  claim_exceptions: number
  provider_contract_issues: number
  compliance_gaps: number
}

export interface Patient {
  id: number
  member_id: string
  name: string
  plan_id: string
  status: string
  risk_category: string
}

export interface Claim {
  id: number
  claim_id: string
  patient_member_id: string
  provider_id: string
  service_date: string
  claim_status: string
  amount: number
  cpt_codes: string[]
  icd_codes: string[]
}

export interface Provider {
  id: number
  provider_id: string
  name: string
  type: string
  network_status: string
}
