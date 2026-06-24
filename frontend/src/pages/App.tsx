import { useEffect, useState } from 'react'
import { getDashboardSummary, runCaseReview, getPatients, getClaims, getProviders } from '../api/client'
import { MetricCard } from '../components/MetricCard'
import type { DashboardSummary, Patient, Claim, Provider } from '../types/ahip'

export function App() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [patients, setPatients] = useState<Patient[]>([])
  const [claims, setClaims] = useState<Claim[]>([])
  const [providers, setProviders] = useState<Provider[]>([])
  const [agentResult, setAgentResult] = useState<any>(null)

  useEffect(() => {
    getDashboardSummary().then(setSummary).catch(console.error)
    getPatients().then(setPatients).catch(console.error)
    getClaims().then(setClaims).catch(console.error)
    getProviders().then(setProviders).catch(console.error)
  }, [])

  async function handleRunAgents() {
    setAgentResult(await runCaseReview('CASE-001'))
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <h1>AHIP</h1>
        <p>AI Healthcare Intelligence Platform</p>
        <p>Agentic AI • Memory • Context • Decisions</p>
      </aside>
      <main className="main">
        <span className="badge">Phase 1 Data Foundation</span>
        <h2>AHIP Operations Dashboard</h2>
        <p>This is the frontend baseline for the healthcare workflow intelligence platform, now powered by the live Phase 1 data models.</p>

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
                <th>ID</th>
                <th>Name</th>
                <th>Plan</th>
                <th>Status</th>
                <th>Risk</th>
              </tr>
            </thead>
            <tbody>
              {patients.map(p => (
                <tr key={p.patient_id}>
                  <td>{p.patient_id}</td>
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
                <th>ID</th>
                <th>Patient</th>
                <th>Provider</th>
                <th>Date</th>
                <th>Status</th>
                <th>Amount</th>
              </tr>
            </thead>
            <tbody>
              {claims.map(c => (
                <tr key={c.claim_id}>
                  <td>{c.claim_id}</td>
                  <td>{c.patient_id}</td>
                  <td>{c.provider_id}</td>
                  <td>{c.service_date}</td>
                  <td>{c.claim_status}</td>
                  <td>${c.amount}</td>
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
                <tr key={p.provider_id}>
                  <td>{p.provider_id}</td>
                  <td>{p.name}</td>
                  <td>{p.type}</td>
                  <td>{p.network_status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </section>

        <section className="section">
          <h3>Sample Multi-Agent Workflow</h3>
          <p>Run a Phase 0 sample case review.</p>
          <button onClick={handleRunAgents}>Run Sample Case Review</button>
          {agentResult && <pre>{JSON.stringify(agentResult, null, 2)}</pre>}
        </section>

        <section className="section">
          <h3>Boundary</h3>
          <p>AHIP is not a chatbot, not a generic RAG system, and not a medical diagnosis tool.</p>
        </section>
      </main>
    </div>
  )
}
