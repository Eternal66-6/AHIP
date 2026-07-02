import { useEffect, useState } from 'react'
import { getAuditLogs } from '../api/client'

export function GovernancePage({ currentUser }: { currentUser: any }) {
  const [auditLogs, setAuditLogs] = useState<any[]>([])

  useEffect(() => {
    getAuditLogs().then(setAuditLogs).catch(console.error)
  }, [])

  return (
    <section className="section">
      <span className="badge">Phase 6</span>
      <h2>Enterprise Governance & Audit Trail</h2>
      <p>Full agent execution trace and manual override history. Visible only to Compliance Officers and Admins.</p>
      
      <div style={{ marginBottom: '15px' }}>
        <strong>Active User:</strong> {currentUser.name} | <strong>Role:</strong> {currentUser.role}
      </div>

      {currentUser.role === "Compliance Officer" ? (
        <table>
          <thead>
            <tr>
              <th>Timestamp</th>
              <th>Case ID</th>
              <th>Action</th>
              <th>Actor</th>
              <th>Details</th>
            </tr>
          </thead>
          <tbody>
            {auditLogs.map(log => (
              <tr key={log.id}>
                <td>{new Date(log.created_at).toLocaleString()}</td>
                <td>{log.case_id}</td>
                <td>
                  <span className="badge" style={{ 
                    background: log.action.includes("OVERRIDE") ? 'rgba(239, 68, 68, 0.2)' : log.action.includes("ACCEPT") ? 'rgba(34, 197, 94, 0.2)' : 'rgba(56, 189, 248, 0.15)',
                    color: log.action.includes("OVERRIDE") ? '#fca5a5' : log.action.includes("ACCEPT") ? '#86efac' : '#38bdf8',
                    border: log.action.includes("OVERRIDE") ? '1px solid rgba(239,68,68,0.3)' : log.action.includes("ACCEPT") ? '1px solid rgba(34,197,94,0.3)' : '1px solid rgba(56,189,248,0.3)'
                  }}>
                    {log.action}
                  </span>
                </td>
                <td>{log.actor}</td>
                <td>{log.details}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <div className="alert-warning">You do not have permission to view the audit trail. Requires Compliance Officer role.</div>
      )}
    </section>
  )
}
