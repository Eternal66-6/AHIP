from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey, JSON
from sqlalchemy.orm import relationship
from .session import Base

class Patient(Base):
    __tablename__ = "patients"
    id = Column(Integer, primary_key=True, index=True)
    member_id = Column(String, unique=True, index=True)
    name = Column(String)
    plan_id = Column(String)
    status = Column(String)
    risk_category = Column(String)

class Provider(Base):
    __tablename__ = "providers"
    id = Column(Integer, primary_key=True, index=True)
    provider_id = Column(String, unique=True, index=True)
    name = Column(String)
    type = Column(String)
    network_status = Column(String)

class Claim(Base):
    __tablename__ = "claims"
    id = Column(Integer, primary_key=True, index=True)
    claim_id = Column(String, unique=True, index=True)
    patient_member_id = Column(String, ForeignKey("patients.member_id"))
    provider_id = Column(String, ForeignKey("providers.provider_id"))
    service_date = Column(Date)
    claim_status = Column(String)
    amount = Column(Integer)
    cpt_codes = Column(JSON)
    icd_codes = Column(JSON)
    
    patient = relationship("Patient", backref="claims")
    provider = relationship("Provider", backref="claims")
