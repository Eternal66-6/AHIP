# AHIP Risks, Assumptions, and Boundaries

This document defines the constraints, boundaries, and risk mitigation strategies for the AHIP platform. These rules ensure the product remains safe, compliant, and focused on operational (rather than clinical) workflows.

---

## 1. Core Platform Boundaries

### A. The Healthcare Safety Boundary (Non-Clinical Rule)
*   **Rule**: AHIP must never provide medical diagnosis, predict disease outcomes, suggest treatments, or recommend prescription medications.
*   **Scope**: The platform operates entirely on the **administrative, operational, and financial layers** of healthcare.
*   **Mitigation**: Any agent prompts or model configurations must include system instructions restricting output to workflow tasks (e.g., "Assign to Provider Network Analyst" or "Request Prior Authorization Form").

### B. Human-in-the-Loop (HITL) Boundary
*   **Rule**: Agents propose recommendations and rank risks, but they do not automatically execute payouts, deny coverage, or adjust contract terms without human approval.
*   **Scope**: All agent actions that impact financial payouts or compliance status must enter a queue for human validation.
*   **Mitigation**: The system's API states must enforce a `USER_APPROVAL` step for all final transactions.

### C. Data Privacy & PHI Boundary
*   **Rule**: The MVP must utilize entirely fictional sample datasets. No real Protected Health Information (PHI) or Personally Identifiable Information (PII) should be loaded into the local or container databases.
*   **Scope**: The demo data consists of generated names, IDs, and fictional billing values.
*   **Mitigation**: Include explicit data masking guides and clean seed scripts in the repository.

---

## 2. Key Operational Assumptions

1.  **Event Availability**: It is assumed that existing payer systems can publish discrete events (like `CLAIM_SUBMITTED` or `PATIENT_DISCHARGED`) in near-real-time.
2.  **Stateless Agent Execution**: Agents themselves are stateless; they receive all context in their dynamic Context Pack, execute, write observations to the database, and terminate.
3.  **PostgreSQL-based Memory**: Complex vector databases are unnecessary for the MVP. A standard PostgreSQL relational database table is sufficient to store agent memory and execution history.
4.  **Deterministic Rules Precedence**: In case of a conflict between an LLM recommendation and a deterministic system database rule (e.g., plan eligibility dates), the database rule takes precedence.

---

## 3. Risk Matrix and Mitigations

| Risk | Impact | Likelihood | Mitigation Strategy |
| :--- | :--- | :--- | :--- |
| **Agent Hallucination** | High | Medium | Enforce structured output schemas (JSON/Pydantic validation) and cross-reference LLM output with deterministic metadata fields (like CPT codes). |
| **Audit Failures** | Critical | Low | Maintain an immutable `AuditLogs` table that records the exact user ID, timestamp, and override reason for every bypassed agent recommendation. |
| **SLA Violations** | Medium | Medium | Implement the `Escalation Agent` to prioritize queues dynamically so that aged cases are highlighted in red for supervisors. |
| **Contract Date Errors** | High | Low | Implement date matching logic inside the `Provider Contract Agent` that compares service dates directly to contract effective dates before running semantic checks. |
