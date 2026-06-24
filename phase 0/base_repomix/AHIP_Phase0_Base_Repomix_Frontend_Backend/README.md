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
