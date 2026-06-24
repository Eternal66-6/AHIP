import { useEffect, useState } from 'react'
import { getDashboardSummary, runCaseReview, getPatients, getClaims, getProviders, getCaseContextMapping } from '../api/client'
import { MetricCard } from '../components/MetricCard'
import type { DashboardSummary, Patient, Claim, Provider } from '../types/ahip'

export function App() {
  const [summary, setSummary] = useState<DashboardSummary | null>(null)
  const [patients, setPatients] = useState<Patient[]>([])
  const [claims, setClaims] = useState<Claim[]>([])
  const [providers, setProviders] = useState<Provider[]>([])
  const [agentResult, setAgentResult] = useState<any>(null)
  
  // Graph mapping state
  const [contextMapping, setContextMapping] = useState<any>(null)
  const [caseIdInput, setCaseIdInput] = useState('CLM2001')

  useEffect(() => {
    getDashboardSummary().then(setSummary).catch(console.error)
    getPatients().then(setPatients).catch(console.error)
    getClaims().then(setClaims).catch(console.error)
    getProviders().then(setProviders).catch(console.error)
  }, [])

  async function handleRunAgents() {
    setAgentResult(await runCaseReview(caseIdInput))
  }

  async function handleViewContextMapping() {
    setContextMapping(await getCaseContextMapping(caseIdInput))
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

        <section className="section">
          <h3>Phase 3: Knowledge Graph Mapping</h3>
          <p>Enter a Claim ID to load the context packs dynamically extracted from the database.</p>
          <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
            <input 
              type="text" 
              value={caseIdInput} 
              onChange={(e) => setCaseIdInput(e.target.value)}
              placeholder="e.g. CLM2001"
            />
            <button onClick={handleViewContextMapping}>View Context Packs</button>
            <button onClick={handleRunAgents}>Run Agents with Memory</button>
          </div>
          {contextMapping && (
             <div className="graph-container">
               <h4>Generated Context Packs for {contextMapping.case_id}</h4>
               <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
                  <div className="box" style={{ background: '#ecfeff', padding: '15px' }}>
                     <h5>🏥 Patient Journey Pack</h5>
                     <pre>{JSON.stringify(contextMapping.patient_journey, null, 2)}</pre>
                  </div>
                  <div className="box" style={{ background: '#fdf4ff', padding: '15px' }}>
                     <h5>📄 Claim Context Pack</h5>
                     <pre>{JSON.stringify(contextMapping.claim, null, 2)}</pre>
                  </div>
                  <div className="box" style={{ background: '#f0fdf4', padding: '15px' }}>
                     <h5>🤝 Provider Contract Pack</h5>
                     <pre>{JSON.stringify(contextMapping.provider_contract, null, 2)}</pre>
                  </div>
                  <div className="box" style={{ background: '#fff7ed', padding: '15px' }}>
                     <h5>🛡️ Compliance Context Pack</h5>
                     <pre>{JSON.stringify(contextMapping.compliance, null, 2)}</pre>
                  </div>
               </div>
             </div>
          )}
          {agentResult && (
             <div style={{ marginTop: '20px' }}>
               <h4>Agent Execution Logs</h4>
               <pre>{JSON.stringify(agentResult, null, 2)}</pre>
             </div>
          )}
        </section>

        <section className="section">
          <h3>Boundary</h3>
          <p>AHIP is not a chatbot, not a generic RAG system, and not a medical diagnosis tool.</p>
        </section>
      </main>
    </div>
  )
}
