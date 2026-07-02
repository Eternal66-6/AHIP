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
