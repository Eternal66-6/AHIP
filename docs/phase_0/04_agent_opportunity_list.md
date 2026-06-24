# AHIP Agent Opportunity List

This document defines the specialized agent registry for the AHIP platform. Each agent is designed as an independent service with a specific focus, clear inputs, structured outputs, memory requirements, and verification criteria.

---

## 1. Patient Journey Agent
*   **Goal**: Monitor patient care transition stages and track timeline progress.
*   **Core Responsibility**: Tracks member status after major events (such as hospital discharges) to ensure they transition smoothly through the care pipeline.
*   **Inputs**: Patient records, workflow event logs, active care tasks.
*   **Outputs**:
    *   Journey status (Stable, Transitioning, Delayed, High-Risk).
    *   List of missing or overdue steps in the care plan.
*   **Memory Requirements**: Patient historical journey observations (writes status changes to `AgentMemory`).
*   **Validation Rules**: Must flag an alert if a patient's transition task is missing or overdue.

---

## 2. Claims Review Agent
*   **Goal**: Identify workflow processing risks and explain why a claim has been pended.
*   **Core Responsibility**: Evaluates pended claims to extract the underlying cause (e.g., missing data, pricing anomalies, coding errors).
*   **Inputs**: Claim, patient, provider, and active contract data.
*   **Outputs**:
    *   Risk Level (Low, Medium, High, Critical).
    *   Observation summary.
    *   Recommendation (e.g., routing to a specific billing queue).
*   **Memory Requirements**: Claim review history (tracks whether this claim has failed audits previously).
*   **Validation Rules**: Output must explicitly list evidence and billing codes.

---

## 3. Provider Contract Agent
*   **Goal**: Ensure provider network parameters and reimbursement rates align with claims.
*   **Core Responsibility**: Compares the provider on a claim with the provider contract registry, verifying network status and date eligibility.
*   **Inputs**: Provider profiles, submitted claims, provider contract records.
*   **Outputs**:
    *   Contract status (Valid, Mapped, date mismatch, out-of-network).
    *   Mismatch alert details (e.g., "Provider billing date is 2026-06-15, but contract expired on 2026-05-31").
*   **Memory Requirements**: Provider contract mapping logs.
*   **Validation Rules**: Any "mismatch" alert must cite the specific contract ID and date bounds.

---

## 4. Benefit Validation Agent
*   **Goal**: Verify member eligibility and coverage rules for requested services.
*   **Core Responsibility**: Evaluates if the service code (CPT) on a claim falls under the member's active Benefit Plan and determines if prior authorization is required.
*   **Inputs**: Benefit plan rules, member eligibility dates, claim service codes.
*   **Outputs**:
    *   Validation status (Approved, Authorization Missing, Limits Exceeded).
    *   Prior authorization required flag.
*   **Memory Requirements**: Member benefit validation logs.
*   **Validation Rules**: Must check prior authorization rules against billing codes without making clinical judgments.

---

## 5. Care Gap Agent
*   **Goal**: Proactively identify missing clinical/operational follow-ups.
*   **Core Responsibility**: Reviews care task deadlines to detect when a patient has missed a post-discharge contact or standard preventive care task.
*   **Inputs**: Care tasks, patient journey events, due dates.
*   **Outputs**:
    *   Care Gap alert (e.g., "Overdue 48h Post-Discharge Call").
    *   Suggested care coordinator owner.
*   **Memory Requirements**: Active and historical care gaps per patient.
*   **Validation Rules**: Must trigger an alert exactly when `due_date < current_time` and `status != 'Completed'`.

---

## 6. Compliance Agent
*   **Goal**: Audit execution histories and ensure proper documentation is in place.
*   **Core Responsibility**: Monitors that pended reviews contain proper evidence and logs user overrides to verify that manual justifications are captured.
*   **Inputs**: Workflow events, agent executions, user override records.
*   **Outputs**:
    *   Compliance status (Compliant, Warn, Non-Compliant).
    *   Audit warnings (e.g., "User override lacks written justification").
*   **Memory Requirements**: Governance audit trail.
*   **Validation Rules**: Every warning must reference the specific event ID or recommendation ID.

---

## 7. Escalation Agent
*   **Goal**: Prioritize pending actions in the queue based on operational risk and SLAs.
*   **Core Responsibility**: Evaluates open cases across all queues, calculating a dynamic priority score so that critical bottlenecks are escalated to supervisors.
*   **Inputs**: All agent outputs, open case ages, SLA thresholds.
*   **Outputs**:
    *   Priority score (1-100).
    *   Escalation tier (Standard, Urgent, Executive).
    *   Recommended supervisor owner.
*   **Memory Requirements**: Escalation trace logs.
*   **Validation Rules**: Priority calculations must be fully explainable (e.g., citing the specific SLA age multiplier).

---

## 8. Workflow Orchestration Agent
*   **Goal**: Coordinate agent execution and compile case-level intelligence.
*   **Core Responsibility**: Acts as the master orchestrator that intercepts workflow events, triggers sub-agents in the correct sequence, collects their observations, and builds a consolidated report.
*   **Inputs**: Workflow event triggers, case database records, agent registry.
*   **Outputs**:
    *   Consolidated Case Intelligence Report (combining risk, contract, benefit, and care gap findings).
*   **Memory Requirements**: Full execution trace (stored in `AgentExecutions`).
*   **Validation Rules**: The execution trace must show timestamps and input/output contracts for every sub-agent called.
