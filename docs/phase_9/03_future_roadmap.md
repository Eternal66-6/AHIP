# AHIP Future Roadmap (Phase 10+)

The current Phase 9 MVP proves the fundamental mechanics of Agentic Healthcare Operations. To evolve this into a commercial, enterprise-grade startup, the following roadmap is proposed.

## Q1: Infrastructure & Scalability
- **Live LLM Integration:** Swap the mock deterministic Python agents for LangChain/LlamaIndex agents powered by Anthropic Claude 3.5 Sonnet (for complex reasoning) and OpenAI GPT-4o-mini (for fast structured extraction).
- **Asynchronous Execution:** Migrate the Multi-Agent pipeline from synchronous HTTP requests to a Celery + Redis task queue. 
- **WebSocket Streaming:** Push live agent execution logs to the React frontend as they happen, eliminating polling delays.

## Q2: Security & Multi-Tenancy
- **Tenant Isolation:** Implement Row-Level Security (RLS) in PostgreSQL so a single database cluster can safely serve multiple distinct healthcare clients.
- **Identity & Access Management (IAM):** Integrate Auth0 for enterprise Single Sign-On (SSO) and map physical JWT claims to FastAPI permission dependencies.
- **PHI Masking Pipeline:** Implement a middleware layer that detects and redacts Protected Health Information (Names, SSNs, exact DOBs) before any payload is sent to an external LLM provider.

## Q3: Ecosystem Integration
- **EHR/Clearinghouse Connectors:** Build generic adapters to pull live claim data via FHIR APIs (e.g., Epic, Cerner) or X12 EDI 837 claim files from clearinghouses like Change Healthcare.
- **Automated Adjudication Actions:** Connect the backend directly to a core claim engine (like QNXT or Facets) so that if AHIP outputs an "Auto-Approve" decision, the claim is instantly paid in the primary system without human intervention.

## Q4: Advanced Agentic Features
- **Dynamic Policy Retrieval:** Implement a Retrieval-Augmented Generation (RAG) vector database (e.g., Pinecone or pgvector) containing the insurer's specific Medical Policies, allowing agents to ground their decisions in live policy documents rather than generalized LLM knowledge.
