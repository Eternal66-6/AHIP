import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { getCaseContextMapping, runCaseReview } from '../api/client'

export function CaseDetailPage() {
  const { caseId } = useParams()
  const [contextMapping, setContextMapping] = useState<any>(null)
  const [agentResult, setAgentResult] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (caseId) {
      getCaseContextMapping(caseId).then(setContextMapping).catch(console.error)
    }
  }, [caseId])

  async function handleRunAgents() {
    if (!caseId) return
    setLoading(true)
    try {
      const result = await runCaseReview(caseId)
      setAgentResult(result)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  if (!caseId) return <div>No case specified</div>

  return (
    <section className="section">
      <span className="badge">Phase 3 & Phase 4</span>
      <h2>Case Detail: {caseId}</h2>
      
      <div style={{ marginBottom: '20px' }}>
        <button onClick={handleRunAgents} disabled={loading}>
          {loading ? "Running Multi-Agent Pipeline..." : "Run Agents with Memory"}
        </button>
      </div>

      {agentResult && (
        <div style={{ marginBottom: '30px' }}>
          <h3>Agent Execution Logs (Phase 4)</h3>
          <pre>{JSON.stringify(agentResult, null, 2)}</pre>
        </div>
      )}

      {contextMapping && (
        <div className="graph-container">
          <h3>Knowledge Graph Mapping (Phase 3)</h3>
          <p>Generated Context Packs for {contextMapping.case_id}</p>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            <div className="box" style={{ background: 'rgba(30, 41, 59, 0.7)', padding: '15px' }}>
              <h5 style={{ margin: '0 0 10px 0', borderBottom: '1px solid #334155', paddingBottom: '10px', color: '#38bdf8' }}>🏥 Patient Journey Pack</h5>
              <pre style={{ margin: 0 }}>{JSON.stringify(contextMapping.patient_journey, null, 2)}</pre>
            </div>
            <div className="box" style={{ background: 'rgba(30, 41, 59, 0.7)', padding: '15px' }}>
              <h5 style={{ margin: '0 0 10px 0', borderBottom: '1px solid #334155', paddingBottom: '10px', color: '#38bdf8' }}>📄 Claim Context Pack</h5>
              <pre style={{ margin: 0 }}>{JSON.stringify(contextMapping.claim, null, 2)}</pre>
            </div>
            <div className="box" style={{ background: 'rgba(30, 41, 59, 0.7)', padding: '15px' }}>
              <h5 style={{ margin: '0 0 10px 0', borderBottom: '1px solid #334155', paddingBottom: '10px', color: '#38bdf8' }}>🤝 Provider Contract Pack</h5>
              <pre style={{ margin: 0 }}>{JSON.stringify(contextMapping.provider_contract, null, 2)}</pre>
            </div>
            <div className="box" style={{ background: 'rgba(30, 41, 59, 0.7)', padding: '15px' }}>
              <h5 style={{ margin: '0 0 10px 0', borderBottom: '1px solid #334155', paddingBottom: '10px', color: '#38bdf8' }}>🛡️ Compliance Context Pack</h5>
              <pre style={{ margin: 0 }}>{JSON.stringify(contextMapping.compliance, null, 2)}</pre>
            </div>
          </div>
        </div>
      )}
    </section>
  )
}
