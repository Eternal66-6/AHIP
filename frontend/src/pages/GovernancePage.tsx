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
                    background: log.action.includes("OVERRIDE") ? '#fee2e2' : log.action.includes("ACCEPT") ? '#dcfce7' : '#e0f2fe',
                    color: log.action.includes("OVERRIDE") ? '#991b1b' : log.action.includes("ACCEPT") ? '#166534' : '#075985'
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
