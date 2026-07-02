import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { getPriorityQueue, submitDecision, getAuditLogs } from '../api/client'

export function PriorityQueuePage({ currentUser }: { currentUser: any }) {
  const [priorityQueue, setPriorityQueue] = useState<any[]>([])
  const navigate = useNavigate()

  useEffect(() => {
    getPriorityQueue().then(setPriorityQueue).catch(console.error)
  }, [])

  async function handleDecision(caseId: string, action: string) {
    try {
      let reason = ""
      if (action === "Override") {
        reason = window.prompt(`Enter reason for manual override on ${caseId}:`) || "No reason provided"
      }
      
      await submitDecision(caseId, action, reason, currentUser.id, currentUser.role)
      setPriorityQueue(prev => prev.filter(item => item.case_id !== caseId))
      alert(`Decision recorded: ${action} for ${caseId}`)
    } catch (e) {
      console.error(e)
    }
  }

  return (
    <section className="section">
      <span className="badge">Phase 5</span>
      <h3>Decision & Escalation Priority Queue</h3>
      <p>This queue displays fully consolidated agent outputs sorted by business impact SLA risk. The AI Recommendation Engine provides full explainability for its routing decisions.</p>
      
      <button onClick={() => getPriorityQueue().then(setPriorityQueue).catch(console.error)} style={{marginBottom: '15px'}}>
        Refresh Priority Queue
      </button>
      
      {priorityQueue.length === 0 ? (
        <p>No pending cases in the priority queue.</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          {priorityQueue.map((item, index) => {
            const isHighRisk = item.routing_destination === "Senior Claims Analyst" || item.routing_destination?.includes("High")
            return (
              <div key={item.id} className="box" style={{ 
                background: isHighRisk ? 'rgba(239, 68, 68, 0.1)' : 'rgba(30, 41, 59, 0.7)',
                borderLeftColor: isHighRisk ? '#ef4444' : '#38bdf8',
                padding: '15px'
              }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <h4 style={{ margin: '0 0 10px 0', color: isHighRisk ? '#fca5a5' : '#38bdf8', cursor: 'pointer', textDecoration: 'underline' }} onClick={() => navigate(`/case/${item.case_id}`)}>
                    Case: {item.case_id} - Queue Rank: #{index + 1}
                  </h4>
                  <span className="badge" style={{ background: isHighRisk ? 'rgba(239, 68, 68, 0.2)' : 'rgba(56, 189, 248, 0.15)', color: isHighRisk ? '#fca5a5' : '#38bdf8', border: isHighRisk ? '1px solid rgba(239,68,68,0.3)' : '1px solid rgba(56,189,248,0.3)' }}>
                    Confidence: {(item.confidence * 100).toFixed(0)}%
                  </span>
                </div>
                
                <p><strong>Routing Destination:</strong> {item.routing_destination}</p>
                <p><strong>Explainability Notes:</strong> {item.summary_observation}</p>
                <p><strong>Action Recommended:</strong> {item.recommended_action}</p>
                
                <div style={{ display: 'flex', gap: '10px', marginTop: '15px' }}>
                  <button 
                    onClick={() => handleDecision(item.case_id, 'Accept')}
                    style={{ background: '#22c55e' }}
                  >
                    Accept Recommendation
                  </button>
                  <button 
                    onClick={() => handleDecision(item.case_id, 'Override')}
                    style={{ background: '#ef4444' }}
                  >
                    Override / Manual Review
                  </button>
                </div>
              </div>
            )
          })}
        </div>
      )}
    </section>
  )
}
