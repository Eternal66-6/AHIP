const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api/v1'

export async function getDashboardSummary() {
  const response = await fetch(`${API_BASE_URL}/dashboard/summary`)
  if (!response.ok) throw new Error('Failed to load dashboard summary')
  return response.json()
}

export async function runCaseReview(caseId: string) {
  const response = await fetch(`${API_BASE_URL}/agents/run-case-review`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ case_id: caseId })
  })
  if (!response.ok) throw new Error('Failed to run agent review')
  return response.json()
}

export async function getPatients() {
  const response = await fetch(`${API_BASE_URL}/patients`)
  if (!response.ok) throw new Error('Failed to load patients')
  return response.json()
}

export async function getClaims() {
  const response = await fetch(`${API_BASE_URL}/claims`)
  if (!response.ok) throw new Error('Failed to load claims')
  return response.json()
}

export async function getProviders() {
  const response = await fetch(`${API_BASE_URL}/providers`)
  if (!response.ok) throw new Error('Failed to load providers')
  return response.json()
}

export async function getCaseContextMapping(caseId: string) {
  const response = await fetch(`${API_BASE_URL}/agents/context/${caseId}`)
  if (!response.ok) throw new Error('Failed to load case context mapping')
  return response.json()
}

export async function getPriorityQueue() {
  const response = await fetch(`${API_BASE_URL}/agents/priority-queue`)
  if (!response.ok) throw new Error('Failed to load priority queue')
  return response.json()
}

export async function submitDecision(caseId: string, action: string, reason?: string, userId?: string, userRole?: string) {
  const response = await fetch(`${API_BASE_URL}/agents/cases/${caseId}/decision`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ action, reason, user_id: userId, user_role: userRole })
  })
  if (!response.ok) throw new Error('Failed to submit decision')
  return response.json()
}

export async function getAuditLogs() {
  const response = await fetch(`${API_BASE_URL}/agents/audit-logs`)
  if (!response.ok) throw new Error('Failed to load audit logs')
  return response.json()
}
