# AHIP Live Demo Script

## 1. Introduction (The Hook)
**Presenter**: "Welcome to AHIP. Healthcare operations are currently drowning in a sea of disconnected data—claims, patient histories, and provider contracts live in separate silos. When a complex claim hits, it takes human analysts 30+ minutes just to gather the context before they can make a decision. Today, I'll show you how AHIP's Agentic AI platform reduces that to zero."

## 2. The Executive Dashboard (The Overview)
**Action**: Open the UI to `/`.
**Presenter**: "Here is the Executive Dashboard. At a glance, leadership can see the volume of Open Cases, High Risk flags, and Compliance Gaps. Below, you see the raw data—patients, claims, and providers. But having data isn't intelligence. Let's look at how AHIP processes this."

## 3. The Priority Queue (The Output)
**Action**: Click on `Priority Queue` in the Sidebar. Click "Refresh Priority Queue".
**Presenter**: "This is the Operations Priority Queue. Instead of a chronological list of claims, our Multi-Agent pipeline has pre-analyzed every case and ranked them by business impact."
**Action**: Point out `CLM2002`.
**Presenter**: "Notice this case at the top, highlighted in red. The AI didn't just route it; it provided explicit Explainability Notes telling us exactly *why* it was escalated to a Senior Claims Analyst."

## 4. Case Details & Agent Pipeline (The 'How')
**Action**: Click on `Case: CLM2002` to navigate to the Case Details page.
**Presenter**: "Let's drill down into CLM2002. How did the AI know this was high risk?"
**Action**: Click "Run Agents with Memory". Wait for the JSON to populate.
**Presenter**: "First, our Context Engine builds a Knowledge Graph. It pulled the Patient's history (Bob Jones is High Risk), the Provider's status (Out-of-Network), and the Claim details ($15,000 for GI surgery). 
Then, our Multi-Agent system takes over. The Claims Agent analyzes the codes, the Compliance Agent flags the Out-of-Network status, and the Consolidator Agent synthesizes it all into a single, definitive routing decision."

## 5. Governance & Override (The Security)
**Action**: Go back to Priority Queue. Click `Override` on CLM2002. Type "Requires manual Medical Director review" in the prompt.
**Presenter**: "AI shouldn't run unchecked. A human analyst can Accept or Override the AI's recommendation. I'm going to override this and provide my justification."
**Action**: Go to `Governance & Audit` in the Sidebar.
**Presenter**: "Because AHIP is an enterprise-grade platform, every single action is logged. Here in the Governance Dashboard, restricted by Role-Based Access Control, auditors can see a permanent, immutable trail of exactly what the AI recommended, and exactly why I overrode it."

## 6. Closing
**Presenter**: "AHIP isn't a chatbot. It's an Agentic workflow intelligence platform that turns raw healthcare data into auditable, actionable operations."
