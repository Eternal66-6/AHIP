# AHIP Phase 0 Research Report: Agentic Healthcare Operations Intelligence

## 1. Introduction to Agentic Healthcare Operations Intelligence
Traditional automation and AI in healthcare have largely fallen into two categories:
1.  **Transactional Systems of Record (EMR/EHR/Payer Systems)**: Excellent at storing massive quantities of data (claims history, provider networks, patient charts) but poor at proactively detecting workflow bottlenecks, coordinating cross-functional actions, or explaining exceptions.
2.  **Conversational Systems (Chatbots/RAG Assistants)**: Great at answering ad-hoc user questions (e.g., "What is the copay for Plan A?") but unable to observe backend events, maintain persistent state, or orchestrate multi-step operational tasks.

**Agentic Healthcare Operations Intelligence** represents a paradigm shift. Rather than waiting for a human to search a database or query a chatbot, a network of specialized, autonomous software units (agents) continuously observes operational events, constructs tailored contexts, collaborates to diagnose complex workflow exceptions, and recommends next-best actions with explainable reasoning.

---

## 2. Why Chatbots and Generic RAG Fail in Healthcare Operations

Healthcare payers and providers manage highly structured, regulated, and context-dependent workflows. Standard Chatbot and Retrieval-Augmented Generation (RAG) architectures fail here for several key reasons:

| Failure Mode | Chatbots / Generic RAG | Agentic Operations Intelligence |
| :--- | :--- | :--- |
| **Trigger Mechanism** | **Reactive**: Only runs when a human types a prompt. | **Proactive**: Event-driven; triggers automatically when a claim is pended or a care task is missed. |
| **Context Scope** | **Global/Noisy**: Pulls raw documents containing excess information, causing hallucinations or token overflow. | **Curated/Minimal**: Uses a Context Builder to deliver structured context packs containing *only* the specific data needed. |
| **Logic Consistency** | **Probabilistic Text**: Generates general answers that may violate strict payer rules or contract terms. | **Rule-Assisted / Structured**: Combines LLM reasoning with deterministic compliance rules and structured schema outputs. |
| **Collaboration** | **Isolated**: A single conversation window cannot hand off a case to another specialized system. | **Collaborative**: Agents communicate via handoff protocols and a shared memory layer to build a unified solution. |
| **State & Memory** | **Ephemeral**: Context is lost once the session ends. | **Persistent**: State is stored in a database (memory table) to track the case history and trace past agent decisions. |

---

## 3. The Core Tenets of Agentic Architecture in AHIP

To achieve coordinated, audit-ready operational decisions, AHIP relies on three core design principles:

### A. Context Engineering (Context Packs)
To prevent agents from hallucinating or slowing down due to large payloads, the system implements **Context Packs**. A Context Pack is a curated bundle of database records assembled specifically for an agent's task. For example:
*   *Claims Review Context*: Includes *only* the target claim, patient profile, provider details, active contract, and related claim history.
*   *Care Gap Context*: Includes *only* the patient journey logs, care tasks, and discharge records.

### B. Structured Memory
Rather than storing memory in complex vector databases (which introduces retrieval uncertainty), AHIP uses **Structured Memory** tables in PostgreSQL. This allows agents to:
*   Write clear, structured observations at the case level.
*   Read previous observations from other agents working on the same case.
*   Provide a persistent, readable log of what each agent determined at any given step in the workflow timeline.

### C. Rule-Assisted Decision Intelligence
Agents generate structured proposals (containing confidence scores and evidence lists), which are then evaluated against deterministic business logic (e.g., SLA timers, contract network rules, authorization requirements). This ensures that while the agent provides semantic reasoning, the system maintains strict operational compliance.

---

## 4. Operational Focus Areas
AHIP focuses on administrative, contractual, and workflow-level challenges:
*   **Claims Auditing & Review**: Detecting why claims are stuck in "Pended" status (e.g., missing contract rates, out-of-network provider mismatches).
*   **Contract Alignment**: Verifying that providers are correctly matched to active contracts based on effective dates and network parameters.
*   **Benefit & Authorization Validation**: Checking if submitted claims correspond to active member benefits and verify if required prior authorizations exist.
*   **Care Coordination Tracking**: Tracking discharge transitions and ensuring timely follow-up tasks are completed to prevent readmission.
