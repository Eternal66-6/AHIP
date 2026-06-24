from datetime import date
from .session import SessionLocal
from .models import Patient, Provider, Claim, Base
from .session import engine

def seed_data():
    db = SessionLocal()
    
    # Check if we already have data
    if db.query(Patient).first():
        db.close()
        return

    print("Seeding database...")

    # Seed Patients
    p1 = Patient(patient_id="PT1001", name="Sarah Jenkins", plan_id="PLN-GOLD-01", status="Active", risk_category="High")
    p2 = Patient(patient_id="PT1002", name="Marcus Cole", plan_id="PLN-SLVR-02", status="Inactive", risk_category="Low")
    p3 = Patient(patient_id="PT1003", name="Elena Rodriguez", plan_id="PLN-BRNZ-03", status="Active", risk_category="Medium")
    db.add_all([p1, p2, p3])

    # Seed Providers
    pr1 = Provider(provider_id="PR2001", name="City General Hospital", type="Facility", network_status="In-Network")
    pr2 = Provider(provider_id="PR2002", name="Dr. James Wilson", type="Individual", network_status="Out-of-Network")
    db.add_all([pr1, pr2])
    db.commit()

    # Seed Claims
    c1 = Claim(claim_id="CLM3001", patient_id="PT1001", provider_id="PR2001", service_date=date(2023, 10, 15), claim_status="Pending", amount=1250.00)
    c2 = Claim(claim_id="CLM3002", patient_id="PT1002", provider_id="PR2002", service_date=date(2023, 10, 16), claim_status="Denied", amount=450.00)
    c3 = Claim(claim_id="CLM3003", patient_id="PT1003", provider_id="PR2001", service_date=date(2023, 10, 18), claim_status="Approved", amount=150.00)
    db.add_all([c1, c2, c3])

    db.commit()
    db.close()
    print("Database seeded successfully.")

def init_db():
    Base.metadata.create_all(bind=engine)
    seed_data()

if __name__ == "__main__":
    init_db()
