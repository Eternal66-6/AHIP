# AHIP MVP Known Limitations

The current Phase 8 build is a fully functional engineering baseline and UX prototype. However, it contains several intentional boundaries to ensure it remains a safe, scoped MVP.

## 1. Mock Deterministic Agents
**Limitation:** The AI agents currently use hard-coded deterministic logic in Python (e.g., `if "Out-of-Network" in context`) rather than making live API calls to an LLM provider like OpenAI or Anthropic. 
**Why:** To ensure predictable, fast demonstrations without requiring API keys, managing rate limits, or risking hallucinations during live demos.

## 2. No Live Auth
**Limitation:** The current user is mocked in the frontend React state.
**Why:** Implementing Auth0/Cognito adds significant setup overhead for reviewers who just want to `docker compose up` and see the platform. 

## 3. Ephemeral Database
**Limitation:** While Postgres is used, the data is generated fresh via a seed script every time the volume is wiped, and the database relies on Docker's local volumes rather than a managed RDS instance.
**Why:** Keeps the repository 100% self-contained and reproducible.

## 4. No Live Clinical Rules Engine
**Limitation:** The platform mocks out CPT/ICD code validation rather than integrating with a massive, expensive healthcare clearinghouse API (like Change Healthcare or Optum).
**Why:** This platform demonstrates the *Agentic orchestration* of that data, not the underlying medical coding logic itself.

## 5. Security Note: Do NOT Use For Real PHI
**CRITICAL WARNING:** This codebase is an educational MVP. Do not insert real Protected Health Information (PHI) or attempt to deploy this to production without completing the items listed in the `04_saas_readiness.md` checklist.
