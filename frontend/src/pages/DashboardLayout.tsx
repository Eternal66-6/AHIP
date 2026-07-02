import { NavLink, Outlet } from 'react-router-dom'
import { LayoutDashboard, ListOrdered, FileSearch, ShieldAlert } from 'lucide-react'

export function DashboardLayout() {
  return (
    <div className="app">
      <aside className="sidebar">
        <h1>AHIP</h1>
        <p>AI Healthcare Intelligence Platform</p>
        
        <nav style={{ marginTop: '40px' }}>
          <NavLink to="/" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            <LayoutDashboard /> Executive Dashboard
          </NavLink>
          
          <NavLink to="/case/CLM2001" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            <FileSearch /> Case Details
          </NavLink>

          <NavLink to="/queue" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            <ListOrdered /> Priority Queue
          </NavLink>
          
          <NavLink to="/governance" className={({ isActive }) => isActive ? "nav-link active" : "nav-link"}>
            <ShieldAlert /> Governance & Audit
          </NavLink>
        </nav>
        
      </aside>
      
      <main className="main">
        <Outlet />
      </main>
    </div>
  )
}
