# AHIP Phase 1 - Seed Dataset

This dataset is automatically populated when the backend application starts with an empty database. All data is fictional and designed for testing MVP scenarios.

## Patients
| patient_id | name | plan_id | status | risk_category |
| :--- | :--- | :--- | :--- | :--- |
| PT1001 | Sarah Jenkins | PLN-GOLD-01 | Active | High |
| PT1002 | Marcus Cole | PLN-SLVR-02 | Inactive | Low |
| PT1003 | Elena Rodriguez | PLN-BRNZ-03 | Active | Medium |

## Providers
| provider_id | name | type | network_status |
| :--- | :--- | :--- | :--- |
| PR2001 | City General Hospital | Facility | In-Network |
| PR2002 | Dr. James Wilson | Individual | Out-of-Network |

## Claims
| claim_id | patient_id | provider_id | service_date | claim_status | amount |
| :--- | :--- | :--- | :--- | :--- | :--- |
| CLM3001 | PT1001 | PR2001 | 2023-10-15 | Pending | $1250.00 |
| CLM3002 | PT1002 | PR2002 | 2023-10-16 | Denied | $450.00 |
| CLM3003 | PT1003 | PR2001 | 2023-10-18 | Approved | $150.00 |
