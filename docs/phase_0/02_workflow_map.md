# Healthcare Payer Workflow Map

This document outlines the operational pipelines and event flows within the AHIP platform. AHIP is event-driven; events move cases through lifecycle stages and trigger specialized agents to analyze data and recommend actions.

---

## 1. Claims Lifecycle event Flow

The diagram below details the path of a claim from provider submission to final payout/rejection, highlighting key trigger points where agents intervene to review anomalies.

```mermaid
graph TD
    A["Provider Submits Claim"] --> B["Event: CLAIM_SUBMITTED"]
    B --> C["Verify Member Eligibility"]
    C -- "Eligible" --> D["Verify Benefit Coverage"]
    C -- "Not Eligible" --> E["Event: CLAIM_DENIED (Eligibility)"]
    
    D -- "Covered" --> F["Check Prior Authorization Rules"]
    D -- "Not Covered" --> G["Event: CLAIM_DENIED (Benefits)"]
    
    F -- "Auth Required & Present" --> H["Apply Provider Contract Pricing"]
    F -- "Auth Required & Missing" --> I["Event: BENEFIT_AUTH_REQUIRED"]
    I --> J["Claims Review Agent & Benefit Validation Agent activated"]
    J --> K["Event: CLAIM_PENDED"]
    
    H --> L["Match Provider Network & Contract Dates"]
    L -- "Active Contract Matched" --> M["Calculate Pricing & Rates"]
    L -- "No Contract/Date Mismatch" --> N["Event: PROVIDER_CONTRACT_MISSING"]
    N --> O["Provider Contract Agent activated"]
    O --> K
    
    M --> P["Event: CLAIM_APPROVED"]
    P --> Q["Generate Explanation of Benefits (EOB)"]
    Q --> R["Disburse Payment"]
    
    K --> S["Case Queue (Human-in-the-Loop Review)"]
    S -- "Override (Reason Documented)" --> T["Event: USER_OVERRIDE_RECOMMENDATION"]
    T --> P
    S -- "Reject" --> U["Event: CLAIM_DENIED (Manual)"]
```

---

## 2. Care Coordination event Flow

This diagram details how care gaps are identified, tracked, and escalated if post-discharge actions are delayed.

```mermaid
graph TD
    A["Patient Discharged from Facility"] --> B["Event: PATIENT_DISCHARGED"]
    B --> C["Generate Discharge Follow-up Care Task"]
    C --> D["Task: 48-Hour Care Transition Phone Call (Status: Pending)"]
    
    D --> E{"Is Task Completed Within 48 Hours?"}
    E -- "Yes" --> F["Event: CARE_TASK_COMPLETED"]
    F --> G["Update Patient Journey Status (Stable)"]
    
    E -- "No" --> H["Event: CARE_TASK_OVERDUE"]
    H --> I["Care Gap Agent activated"]
    I --> J["Create Care Gap Alert & Update Risk Category"]
    J --> K["Event: CASE_AGED_OVER_THRESHOLD"]
    K --> L["Escalation Agent activated"]
    L --> M["Escalate case to Care Coordinator Lead"]
```

---

## 3. Core Event Triggers & Handoffs

In the AHIP platform, events serve as the glue between modules:
1.  **Ingestion**: A system database change or message queue publishes a `CLAIM_SUBMITTED` event.
2.  **Orchestration**: The `Workflow Orchestration Agent` intercept this event, builds a `Claim Context Pack`, and triggers the `Claims Review Agent` and `Benefit Validation Agent` in parallel.
3.  **Observation**: If either agent detects a discrepancy (e.g., a missing PA document or a missing contract mapping), it emits an anomaly event (`BENEFIT_AUTH_REQUIRED` or `PROVIDER_CONTRACT_MISSING`).
4.  **Escalation**: These anomaly events change the claim status to `PENDED` and trigger the `Escalation Agent` to calculate risk prioritization.
5.  **Audit**: Any human operational decision (e.g., overriding a pended state) triggers a `USER_OVERRIDE_RECOMMENDATION` event, which writes a permanent record to the `AuditLogs` table.
