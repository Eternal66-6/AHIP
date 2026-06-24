from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from .session import Base

class Patient(Base):
    __tablename__ = "patients"
    patient_id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    plan_id = Column(String)
    status = Column(String)
    risk_category = Column(String)

class Provider(Base):
    __tablename__ = "providers"
    provider_id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)
    type = Column(String)
    network_status = Column(String)

class Claim(Base):
    __tablename__ = "claims"
    claim_id = Column(String, primary_key=True, index=True)
    patient_id = Column(String, ForeignKey("patients.patient_id"))
    provider_id = Column(String, ForeignKey("providers.provider_id"))
    service_date = Column(Date)
    claim_status = Column(String)
    amount = Column(Float)
    
    patient = relationship("Patient", backref="claims")
    provider = relationship("Provider", backref="claims")
