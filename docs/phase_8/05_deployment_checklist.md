# AHIP Deployment Checklist

For demonstrating this MVP locally or on a standard cloud VM, follow this checklist.

## Prerequisites
- [x] Docker installed (v20+)
- [x] Docker Compose installed (v2+)
- [x] Port 8000 (Backend) open and available
- [x] Port 5173 (Frontend) open and available

## Environment Setup
- [ ] Rename `.env.example` to `.env` (if applicable) or ensure default mock values are set.
- [ ] Ensure `DATABASE_URL` in `docker-compose.yml` points to the internal Docker network `postgresql+psycopg2://ahip:ahip_password@postgres:5432/ahip_db`.

## Build & Run
- [ ] Run `docker compose down -v` to clear any old volumes and ensure a clean slate.
- [ ] Run `docker compose up --build -d` to spin up the Postgres, Backend, and Frontend containers.
- [ ] Verify `docker ps` shows all three containers in an `Up` status.
- [ ] Run `docker logs ahip-backend-1` to verify the `seed.py` script ran successfully and populated the database.

## Smoke Testing
- [ ] Hit `http://localhost:8000/docs` to verify the FastAPI Swagger UI is active.
- [ ] Hit `http://localhost:5173/` to verify the React frontend loads.
- [ ] Click "Refresh Priority Queue" to ensure the frontend can successfully communicate with the backend API and database.
