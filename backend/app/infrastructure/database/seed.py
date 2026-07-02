import logging
from datetime import date
from .session import engine, Base, SessionLocal
from .models import Patient, Provider, Claim

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def seed_db():
    logger.info("Dropping all tables to ensure clean state...")
    Base.metadata.drop_all(bind=engine)
    logger.info("Creating tables...")
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(Patient).count() == 0:
            logger.info("Seeding patients...")
            p1 = Patient(member_id="MEM1001", name="Alice Smith", plan_id="PLAN_A_GOLD", status="Active", risk_category="Standard")
            p2 = Patient(member_id="MEM1002", name="Bob Jones", plan_id="PLAN_A_GOLD", status="Active", risk_category="High")
            p3 = Patient(member_id="MEM1003", name="Charlie Brown", plan_id="PLAN_B_SILVER", status="Active", risk_category="Standard")
            p4 = Patient(member_id="MEM1004", name="Diana Prince", plan_id="PLAN_C_BRONZE", status="Active", risk_category="Critical")
            p5 = Patient(member_id="MEM1005", name="Evan Wright", plan_id="PLAN_A_GOLD", status="Inactive", risk_category="Low")
            db.add_all([p1, p2, p3, p4, p5])
            
            logger.info("Seeding providers...")
            pr1 = Provider(provider_id="NPI1000003", name="City General Hospital", type="Facility", network_status="In-Network")
            pr2 = Provider(provider_id="NPI1000001", name="Dr. James Wilson", type="Individual", network_status="Out-of-Network")
            pr3 = Provider(provider_id="NPI1000005", name="Westside Clinic", type="Facility", network_status="In-Network")
            pr4 = Provider(provider_id="NPI1000009", name="Dr. Sarah Connor", type="Individual", network_status="Suspended")
            db.add_all([pr1, pr2, pr3, pr4])

            db.commit()

            logger.info("Seeding claims...")
            c1 = Claim(
                claim_id="CLM2001", 
                patient_member_id="MEM1001", 
                provider_id="NPI1000003", 
                service_date=date(2023, 10, 1), 
                claim_status="Pended", 
                amount=250,
                cpt_codes=["99213"],
                icd_codes=["J01.90"]
            )
            c2 = Claim(
                claim_id="CLM2002", 
                patient_member_id="MEM1002", 
                provider_id="NPI1000001", 
                service_date=date(2023, 10, 5), 
                claim_status="Submitted", 
                amount=15000,
                cpt_codes=["43239", "00811"],
                icd_codes=["K21.9"]
            )
            c3 = Claim(
                claim_id="CLM2003", 
                patient_member_id="MEM1004", 
                provider_id="NPI1000009", 
                service_date=date(2023, 10, 8), 
                claim_status="Denied", 
                amount=8500,
                cpt_codes=["70450"],
                icd_codes=["R51"]
            )
            c4 = Claim(
                claim_id="CLM2004", 
                patient_member_id="MEM1003", 
                provider_id="NPI1000005", 
                service_date=date(2023, 10, 12), 
                claim_status="Approved", 
                amount=120,
                cpt_codes=["99212"],
                icd_codes=["Z00.00"]
            )
            c5 = Claim(
                claim_id="CLM2005", 
                patient_member_id="MEM1005", 
                provider_id="NPI1000003", 
                service_date=date(2023, 10, 15), 
                claim_status="Pended", 
                amount=4500,
                cpt_codes=["27447"],
                icd_codes=["M16.1"]
            )
            db.add_all([c1, c2, c3, c4, c5])
            db.commit()
            
            logger.info("Database seeded successfully.")
        else:
            logger.info("Database already seeded.")
    except Exception as e:
        logger.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_db()
