# AHIP SaaS Readiness Roadmap

To transition AHIP from an MVP Agentic Demo into a production-ready Multi-Tenant SaaS, the following architecture upgrades are required.

## 1. Multi-Tenancy & Data Isolation
Currently, all data lives in a single Postgres schema. 
- **Requirement:** Implement Row-Level Security (RLS) in Postgres.
- **Requirement:** Add a `tenant_id` column to all tables (`patients`, `claims`, `providers`, `audit_logs`).
- **Requirement:** Inject the `tenant_id` into the SQLAlchemy session context so that queries automatically filter by tenant.

## 2. Authentication & Authorization (RBAC)
Currently, the active user is mocked in React state (`const [currentUser] = useState(...)`).
- **Requirement:** Integrate an identity provider (Auth0, Okta, or AWS Cognito).
- **Requirement:** Secure the FastAPI endpoints using JWT token validation (`Depends(verify_token)`).
- **Requirement:** Map JWT claims (e.g., `role: compliance_officer`) to the FastAPI route permissions.

## 3. HIPAA & SOC2 Compliance
- **Requirement:** Encrypt all PHI (Protected Health Information) at rest using AWS KMS or Postgres pgcrypto.
- **Requirement:** Mask PII/PHI in the Agentic Logs. LLM prompts must strip names and exact birthdates before hitting the OpenAI/Anthropic API, replacing them with generic tokens (e.g., `[PATIENT_A]`).
- **Requirement:** Ensure the `AuditLog` table is strictly append-only and replicated to secure cold-storage.

## 4. Agentic AI Scalability
Currently, agents run synchronously via a standard HTTP request loop.
- **Requirement:** Move the Multi-Agent pipeline to an asynchronous task queue (e.g., Celery + Redis).
- **Requirement:** Implement webhooks or WebSockets to notify the React frontend when an agent finishes processing a case, rather than blocking the HTTP response.
