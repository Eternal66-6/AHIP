# AHIP – Phase 0 Base Repomix

AI Healthcare Intelligence Platform – frontend and backend baseline.

This repository is the mandatory **Phase 0 Engineering Baseline** for AHIP.

It provides:

- Python FastAPI backend
- React + TypeScript frontend
- PostgreSQL-ready clean architecture
- Agent layer placeholders
- Context layer placeholder
- Decision layer placeholder
- Dashboard shell
- Docker Compose foundation
- Engineering baseline feeder document

## Phase Deliverables

### Phase 0
The research and analysis deliverables for Phase 0 are documented here:
- **Research Report**: [01_research_report.md](file:///c:/Users/Ananthakrishnan%20A%20H/Desktop/Ahip/docs/phase_0/01_research_report.md)
- **Healthcare Payer Workflow Map**: [02_workflow_map.md](file:///c:/Users/Ananthakrishnan%20A%20H/Desktop/Ahip/docs/phase_0/02_workflow_map.md)
- **Domain Glossary**: [03_domain_glossary.md](file:///c:/Users/Ananthakrishnan%20A%20H/Desktop/Ahip/docs/phase_0/03_domain_glossary.md)
- **Agent Opportunity List**: [04_agent_opportunity_list.md](file:///c:/Users/Ananthakrishnan%20A%20H/Desktop/Ahip/docs/phase_0/04_agent_opportunity_list.md)
- **Sample MVP Scenarios**: [05_sample_mvp_scenarios.md](file:///c:/Users/Ananthakrishnan%20A%20H/Desktop/Ahip/docs/phase_0/05_sample_mvp_scenarios.md)
- **Risks and Boundaries**: [06_risks_and_boundaries.md](file:///c:/Users/Ananthakrishnan%20A%20H/Desktop/Ahip/docs/phase_0/06_risks_and_boundaries.md)

### Phase 1: Platform Foundation & Data Model
- ✅ Initialized PostgreSQL schema with explicit constraints and seeded real mock healthcare data.
- ✅ Exposed REST APIs covering Patients, Claims, and Providers.
- ✅ Hooked dynamic React frontend tables directly to Live Database models.

### Phase 2: First Agent Development
- ✅ Converted static mock agents into advanced deterministic logic querying live database rows.
- ✅ Implemented `AgentExecutionLog` to create persistent Agent Memory.
- ✅ Validated full execution loop via `/api/v1/agents/run-case-review` and logged insights via `/api/v1/agents/logs`.

### Phase 3: Knowledge Layer & Context Engineering
- ✅ Designed strictly typed Pydantic Context Packs (`PatientJourneyContextPack`, `ClaimContextPack`, etc.) for precise Context Minimization.
- ✅ Refactored `HealthcareContextBuilder` to map raw database models into dedicated Context Packs for each agent.
- ✅ Added a visual Knowledge Graph Mapping UI to the React frontend to display dynamic Context Packs.

## What AHIP Is

AHIP is an Agentic Healthcare Operations Intelligence Platform.

It is not:

- a chatbot
- a generic RAG app
- a medical diagnosis system

## Stack

| Layer | Technology |
|---|---|
| Frontend | React + TypeScript + Vite |
| Backend | Python FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Agent Layer | Python services |
| Memory | PostgreSQL tables |
| Deployment | Docker Compose |

## Run

```bash
docker compose up --build
```

Backend: http://localhost:8000/docs  
Frontend: http://localhost:5173
