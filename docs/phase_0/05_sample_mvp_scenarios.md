# AHIP Sample MVP Scenarios

This document details the core end-to-end operational scenarios that the AHIP MVP must support, using the seed datasets and agent orchestration services.

---

## Scenario 1: Claim Pending Due to Missing Provider Contract Mapping

### 1. Scenario Description
A provider submits a claim for a member's visit. When processing the claim, the system is unable to match the billing rate because the provider's active contract mapping has expired or does not exist for the service date.

### 2. Event Sequence & Trigger
1.  An event `CLAIM_SUBMITTED` is published.
2.  The `Workflow Orchestration Agent` builds the context pack and runs the `Provider Contract Agent` and `Claims Review Agent`.
3.  The `Provider Contract Agent` checks the `provider_contracts` table and finds that the provider's contract ended on `2026-05-31`, but the claim's `service_date` is `2026-06-15`.
4.  The agent publishes a `PROVIDER_CONTRACT_MISSING` event and logs the observation: *"Claim service date falls outside provider contract date bounds."*
5.  The claim status is updated to `PENDED` and a `CLAIM_PENDED` event is published.

### 3. Recommended Action
*   Route the claim to the **Provider Contract Analyst Queue**.
*   Generate an explainable task: *"Contract ID CON-789 expired on 2026-05-31. Contact provider network team to verify renewal status."*

---

## Scenario 2: Claim Requires Prior Authorization but Document is Missing

### 1. Scenario Description
A provider submits a claim for a high-cost MRI scan. The member's benefit plan requires prior authorization for this billing code (CPT 72148), but no active authorization record is attached to the member's profile.

### 2. Event Sequence & Trigger
1.  An event `CLAIM_SUBMITTED` is published.
2.  The `Workflow Orchestration Agent` runs the `Benefit Validation Agent`.
3.  The `Benefit Validation Agent` queries `benefit_plans` and detects that MRI codes require authorization (`auth_required = true`). It then queries the authorization table and finds no matching record.
4.  The agent publishes a `BENEFIT_AUTH_REQUIRED` event and logs the observation: *"CPT 72148 requires prior authorization, but no active auth record was found for patient."*
5.  The claim status is updated to `PENDED` and a `CLAIM_PENDED` event is published.

### 3. Recommended Action
*   Route the claim to the **Prior Authorization Review Queue**.
*   Generate an explainable task: *"MRI scan requires prior authorization. Request authorization form from provider clinic or check member document portal."*

---

## Scenario 3: Patient Follow-Up Task Overdue (Care Gap)

### 1. Scenario Description
A high-risk member is discharged from a facility with congestive heart failure. A care task is generated for a transition coordinator to call the patient within 48 hours. The coordinator fails to make the call before the SLA expires.

### 2. Event Sequence & Trigger
1.  On patient discharge, a `PATIENT_DISCHARGED` event is published.
2.  A care task is created in the database: `task_id = TASK-404`, `due_date = 2026-06-18 12:00:00`, `status = Pending`.
3.  A cron job or event listener detects that the current time has passed the due date and the task is still pending. It publishes a `CARE_TASK_OVERDUE` event.
4.  The `Care Gap Agent` is activated, queries the patient timeline, and publishes a `CARE_GAP_ALERT` event: *"Overdue discharge follow-up call. Member readmission risk is High."*

### 3. Recommended Action
*   Update the patient's `risk_category` to `High`.
*   Route the case to the **Care Coordinator Escalation Queue**.
*   Generate an urgent recommendation: *"Conduct immediate post-discharge wellness call. Task is 24 hours overdue."*

---

## Scenario 4: Case Aged Beyond Threshold (SLA Escalation)

### 1. Scenario Description
A claim has been pended in the contract review queue for over 10 days. This exceeds the standard operational SLA of 7 days, creating an operational backlog risk.

### 2. Event Sequence & Trigger
1.  An audit listener or batch job checks open pended claims and detects a claim open for 11 days.
2.  It publishes a `CASE_AGED_OVER_THRESHOLD` event.
3.  The `Escalation Agent` is activated, retrieves the pended claim and previous agent logs, and calculates an escalation priority score of `92/100` (Tier: Urgent).
4.  The agent publishes an escalation recommendation: *"Claim CLAIM-101 has been pended for 11 days in the Provider Contract queue. SLA is breached."*

### 3. Recommended Action
*   Reassign the case owner from "Analyst" to "Operations Supervisor".
*   Highlight the claim in red in the supervisor's dashboard queue.

---

## Scenario 5: Agent Recommendation Overridden by User

### 1. Scenario Description
The `Benefit Validation Agent` recommends denying a claim because a prior authorization document is missing. However, a claims manager reviews the case, notes that it was an emergency life-saving procedure, and manually approves the claim, bypassing the restriction.

### 2. Event Sequence & Trigger
1.  The claims manager clicks "Approve with Override" in the UI.
2.  The UI prompts the user to enter an override reason. The user submits: *"Emergency procedure (Section 4.2 bypass rules apply)."*
3.  An event `USER_OVERRIDE_RECOMMENDATION` is published.
4.  The `Compliance Agent` is activated, audits the override transaction, and writes an entry to the `AuditLogs` table:
    *   `action = OVERRIDE_BENEFIT_RULE`
    *   `override_reason = Emergency procedure (Section 4.2 bypass rules apply)`
    *   `user_id = USER-88`
    *   `status = Compliant (Audit trail complete)`

### 3. Recommended Action
*   Log the transaction in the compliance audit trail.
*   Update claim status to `APPROVED` and trigger payment processing.
