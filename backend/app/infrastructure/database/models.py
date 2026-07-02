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

class AgentExecutionLog(Base):
    __tablename__ = "agent_execution_logs"
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String, index=True)
    agent_name = Column(String)
    input_summary = Column(String)
    observation = Column(String)
    recommendation = Column(String)
    confidence = Column(Float)
    related_workflow_event = Column(String, nullable=True)
    created_at = Column(String) # We'll just store ISO strings for simplicity, or use DateTime. Let's use String for SQLite ease.
    
    # Phase 6 Governance fields
    decision_status = Column(String, default="PENDING") # PENDING, ACCEPTED, OVERRIDDEN
    decision_reason = Column(String, nullable=True)
    decided_by = Column(String, nullable=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(String, index=True)
    action = Column(String) # e.g. "AGENT_EXECUTION", "DECISION_ACCEPTED", "DECISION_OVERRIDDEN"
    actor = Column(String) # e.g. "Consolidator Agent", or Human User ID
    details = Column(String)
    created_at = Column(String)
