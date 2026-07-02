# AHIP Architecture Documentation

AHIP is designed to decouple raw healthcare data from intelligent operations, utilizing a Multi-Agent architecture to process, analyze, and route tasks.

## System Components

### 1. Data Layer (PostgreSQL & SQLAlchemy)
The foundational layer holding normalized healthcare data.
- **Models:** `Patient`, `Provider`, `Claim`, `AuditLog`.
- **Function:** Acts as the single source of truth. Does not contain any AI logic or unstructured JSON.

### 2. Context Engine (The Bridge)
The critical translation layer between structured data and LLM tokens.
- **Implementation:** `backend/app/domain/context_engine.py`
- **Function:** Takes raw database rows and aggressively minimizes them into JSON "Context Packs". This prevents sending unnecessary tokens to the LLM (reducing latency and cost) while maximizing the signal-to-noise ratio for the agents.

### 3. Multi-Agent Pipeline
The operational brain of AHIP.
- **Claims Agent:** Analyzes the `Claim` and `Patient` context to flag high-risk procedures or financial anomalies.
- **Compliance Agent:** Analyzes the `Provider` context to flag network suspensions or contract violations.
- **Shared Memory:** Both agents write their findings into a single, isolated state dictionary.
- **Consolidator Agent:** Reads the Shared Memory and makes a final, deterministic routing decision (e.g., "Auto-Adjudicate" vs "Escalate to Senior Analyst").

### 4. API & Orchestration (FastAPI)
The RESTful interface connecting the frontend to the backend.
- **Endpoints:** `/priority-queue` (Agent output), `/decision` (Human override/Governance).

### 5. Client Layer (React)
A modular, glassmorphic UI designed for operational efficiency.
- **Routing:** `react-router-dom` enables deep-linking directly from a Priority Queue alert to a Case Details workspace.
- **UX:** Merges the Context Engine's raw data and the Multi-Agent pipeline's execution logs into a single, cohesive human-in-the-loop dashboard.
