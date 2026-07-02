# AHIP Domain Glossary

This glossary establishes the common language and ontology used across the AHIP system database, backend APIs, and agent reasoning contexts.

---

## 1. Core Healthcare Payer Entities

*   **Member / Patient**: An individual enrolled in a health insurance plan who is eligible to receive covered healthcare services. Key attributes include `patient_id`, `plan_id`, and `risk_category`.
*   **Provider**: A doctor, hospital, clinic, therapist, or medical facility licensed to deliver healthcare services. Attributes include `provider_id`, `network_status` (In-Network/Out-of-Network), and `specialty`.
*   **Claim**: A billing document submitted by a provider to a payer requesting payment for healthcare services rendered to a member. Key fields include `claim_id`, `patient_id`, `provider_id`, `service_date`, `claim_status` (e.g., Submitted, Pended, Approved, Denied), and billing codes (CPT/ICD-10).
*   **Benefit Plan**: A contract between the payer and a member (or sponsor) specifying what medical services are covered, what coverage limits apply, and the financial responsibilities of the member. Attributes include `plan_id`, `auth_required` flags, and `coverage_limits`.
*   **Provider Contract**: A negotiated agreement between the payer and a provider establishing payment rates, billing policies, and network rules. Fields include `contract_id`, `provider_id`, `effective_from`, `effective_to`, and billing multiplier rates.
*   **Operational Provision**: A specific configuration rule or amendment within a provider contract or benefit plan that dictates how claims should be processed under specific circumstances (e.g., out-of-network emergency overrides).
*   **Care Task**: An administrative or care coordination action assigned to a payer's operational staff or care managers to assist a member (e.g., arranging post-discharge transport or conducting a wellness call). Key attributes: `task_id`, `due_date`, `status` (Pending, Completed, Overdue), and `owner`.
*   **Workflow Event**: A timestamped, immutable audit record documenting a state transition or critical occurrence in a payer operation (e.g., `CLAIM_PENDED`, `CARE_TASK_OVERDUE`). Used to trigger agents.

---

## 2. Key Operational Terminology

*   **Pended Claim (Pend)**: A state in which a claim is temporarily held in suspension because it fails automated processing edits or requires manual review (e.g., missing prior authorization, contract date mismatch).
*   **Prior Authorization (PA)**: A benefit plan requirement that forces a provider to obtain approval from the insurer *before* performing a specific service or prescribing a drug, verifying that it is medically necessary and covered.
*   **SLA (Service Level Agreement)**: The legally or operationally mandated timeframe in which a payer must process a claim or resolve an escalation (e.g., clean claims must be paid within 30 days; urgent care tasks resolved within 48 hours).
*   **Network Status**: Indication of whether a provider is contracted with the insurance plan (**In-Network**) or has no formal pricing agreement (**Out-of-Network**). Out-of-network claims typically require separate coverage rules and higher member cost-sharing.
*   **Care Gap**: A discrepancy between a patient's documented care journey and recommended clinical/operational guidelines (e.g., a patient discharged with congestive heart failure who has not received a follow-up call within 48 hours).
*   **Explanation of Benefits (EOB)**: A document sent to the member detailing what portion of a claim was paid to the provider, what was write-off, and what portion is the member's responsibility (copay, deductible, coinsurance).
*   **Human-in-the-Loop (HITL)**: A system design principle requiring that critical decisions (such as overriding contract rules or denying claims) are proposed by agents but must be approved or executed by a human operational analyst.
*   **Override**: A manual action taken by an authorized human analyst that bypasses an agent's recommendation or a standard system business rule. Must be accompanied by a documented reason.
