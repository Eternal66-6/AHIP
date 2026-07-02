# AHIP Phase 1 - Database Schema

The initial MVP uses an SQLite database (configured for local development) via SQLAlchemy ORM.

## Entities

### `patients`
Stores member information and risk categorization.
- `patient_id` (String, Primary Key, Indexed): Unique identifier (e.g., PT1001).
- `name` (String, Indexed): Full name of the patient.
- `plan_id` (String): Benefit plan identifier.
- `status` (String): Patient coverage status (e.g., Active, Inactive).
- `risk_category` (String): Assigned risk category (e.g., High, Medium, Low).

### `providers`
Stores healthcare facility and practitioner information.
- `provider_id` (String, Primary Key, Indexed): Unique identifier (e.g., PR2001).
- `name` (String, Indexed): Name of the facility or doctor.
- `type` (String): Provider type (e.g., Facility, Individual).
- `network_status` (String): Network status (e.g., In-Network, Out-of-Network).

### `claims`
Stores claim records submitted by providers for patient services.
- `claim_id` (String, Primary Key, Indexed): Unique identifier (e.g., CLM3001).
- `patient_id` (String, Foreign Key -> `patients.patient_id`): Associated patient.
- `provider_id` (String, Foreign Key -> `providers.provider_id`): Associated provider.
- `service_date` (Date): Date the service was rendered.
- `claim_status` (String): Status of the claim (e.g., Pending, Approved, Denied).
- `amount` (Float): Billed amount in USD.
