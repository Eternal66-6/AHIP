import { useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { DashboardLayout } from './DashboardLayout'
import { ExecutiveDashboard } from './ExecutiveDashboard'
import { PriorityQueuePage } from './PriorityQueuePage'
import { CaseDetailPage } from './CaseDetailPage'
import { GovernancePage } from './GovernancePage'

export function App() {
  const [currentUser] = useState({ name: "John Doe", role: "Compliance Officer", id: "U-8899" })

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<DashboardLayout />}>
          <Route index element={<ExecutiveDashboard />} />
          <Route path="queue" element={<PriorityQueuePage currentUser={currentUser} />} />
          <Route path="case/:caseId" element={<CaseDetailPage />} />
          <Route path="governance" element={<GovernancePage currentUser={currentUser} />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}
