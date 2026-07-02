# AHIP Engineering Baseline

This file is a mandatory feeder document, similar to a baseline Repomix.

## Non-Negotiable Stack

| Layer | Technology |
|---|---|
| Frontend | React + TypeScript + Vite |
| Backend | Python FastAPI |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Agent Layer | Python services |
| Memory | PostgreSQL tables |
| Context | Context Pack services |
| Decision Layer | Rule-assisted scoring |
| Deployment | Docker Compose |

## Engineering Rules

1. Do not change the stack without approval.
2. Do not convert AHIP into a chatbot.
3. Do not convert AHIP into only a RAG app.
4. Keep agents as separate services/classes.
5. Keep all agent output structured and auditable.
6. Use PostgreSQL for MVP memory.
7. No vector database required for MVP.
8. No GPU required for MVP.
9. Avoid medical diagnosis and treatment recommendations.
10. Keep humans in the loop.

## Clean Architecture Direction

Backend:
- API Layer
- Domain Layer
- Application Layer
- Infrastructure Layer

Frontend:
- API client
- Types
- Components
- Pages
- Utilities
