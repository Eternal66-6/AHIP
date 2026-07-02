# AHIP MVP Demo Dataset

The AHIP platform is seeded with a highly specific mock dataset designed to showcase the Agentic workflow logic in various scenarios. The data is generated on container boot via `backend/app/infrastructure/database/seed.py`.

## Patients
We seed patients across the risk spectrum to demonstrate contextual routing:
- **Alice Smith (Standard)**: Standard active patient, baseline for normal claims processing.
- **Bob Jones (High)**: High-risk patient flag, heavily alters downstream Agent scoring logic.
- **Charlie Brown (Standard)**: Standard active patient.
- **Diana Prince (Critical)**: Triggers immediate SLA alerts for any denied claims.
- **Evan Wright (Low/Inactive)**: Demonstrates handling of inactive patients with historical claims.

## Providers
- **City General Hospital (In-Network Facility)**: Standard institutional billing.
- **Dr. James Wilson (Out-of-Network Individual)**: Triggers contract and out-of-network compliance checks.
- **Westside Clinic (In-Network Facility)**: Clean network provider.
- **Dr. Sarah Connor (Suspended)**: High-risk compliance violation scenario.

## Demonstration Claims
We have crafted 5 specific claims to trigger the Agent pathways:

1. **CLM2001** (Alice / City General): A standard $250 claim for a routine visit. Agent typically routes to auto-adjudication.
2. **CLM2002** (Bob / Dr. Wilson): A $15,000 Out-of-Network claim for a High-Risk patient. This is the **primary demo scenario** that triggers the `Senior Claims Analyst` routing with high SLA severity.
3. **CLM2003** (Diana / Dr. Connor): An $8,500 denied claim from a Suspended provider for a Critical patient. Highlights severe compliance/fraud flags.
4. **CLM2004** (Charlie / Westside Clinic): A clean $120 approved claim for routine checkup.
5. **CLM2005** (Evan / City General): A $4,500 pending claim for an inactive patient (requires historical eligibility verification).
