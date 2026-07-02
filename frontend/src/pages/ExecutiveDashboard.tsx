import { useEffect, useState } from 'react'
import { getDashboardSummary, getPatients, getClaims, getProviders } from '../api/client'
import { MetricCard } from '../components/MetricCard'
import type { DashboardSummary, Patient, Claim, Provider } from '../types/ahip'

export function ExecutiveDashboard() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [patients, setPatients] = useState<Patient[]>([])
  const [claims, setClaims] = useState<Claim[]>([])
  const [providers, setProviders] = useState<Provider[]>([])

  useEffect(() => {
    getDashboardSummary().then(setSummary).catch(console.error)
    getPatients().then(setPatients).catch(console.error)
    getClaims().then(setClaims).catch(console.error)
    getProviders().then(setProviders).catch(console.error)
  }, [])

  return (
    <>
      <span className="badge">Phase 1 Data Foundation</span>
      <h2>AHIP Executive Dashboard</h2>
      <p>This is the frontend baseline for the healthcare workflow intelligence platform, powered by the live Phase 1 data models.</p>

      {summary && (
        <div className="grid">
          <MetricCard label="Open Cases" value={summary.open_cases} />
          <MetricCard label="High Risk" value={summary.high_risk_cases} />
          <MetricCard label="Claim Exceptions" value={summary.claim_exceptions} />
          <MetricCard label="Contract Issues" value={summary.provider_contract_issues} />
          <MetricCard label="Compliance Gaps" value={summary.compliance_gaps} />
        </div>
      )}

      <section className="section">
        <h3>Patients</h3>
        <table>
          <thead>
            <tr>
              <th>Member ID</th>
              <th>Name</th>
              <th>Plan</th>
              <th>Status</th>
              <th>Risk</th>
            </tr>
          </thead>
          <tbody>
            {patients.map(p => (
              <tr key={p.id}>
                <td>{p.member_id}</td>
                <td>{p.name}</td>
                <td>{p.plan_id}</td>
                <td>{p.status}</td>
                <td>{p.risk_category}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="section">
        <h3>Claims</h3>
        <table>
          <thead>
            <tr>
              <th>Claim ID</th>
              <th>Patient Member ID</th>
              <th>Provider ID</th>
              <th>Date</th>
              <th>Status</th>
              <th>Amount</th>
              <th>CPT Codes</th>
              <th>ICD Codes</th>
            </tr>
          </thead>
          <tbody>
            {claims.map(c => (
              <tr key={c.id}>
                <td>{c.claim_id}</td>
                <td>{c.patient_member_id}</td>
                <td>{c.provider_id}</td>
                <td>{c.service_date}</td>
                <td>{c.claim_status}</td>
                <td>${c.amount}</td>
                <td>{c.cpt_codes?.join(', ')}</td>
                <td>{c.icd_codes?.join(', ')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      <section className="section">
        <h3>Providers</h3>
        <table>
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Type</th>
              <th>Network Status</th>
            </tr>
          </thead>
          <tbody>
            {providers.map(p => (
              <tr key={p.id}>
                <td>{p.provider_id}</td>
                <td>{p.name}</td>
                <td>{p.type}</td>
                <td>{p.network_status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </>
  )
}
