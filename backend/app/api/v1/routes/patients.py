from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database.session import get_db
from app.infrastructure.database.models import Patient as PatientModel
from app.domain.schemas.schemas import Patient, PatientBase

router = APIRouter()

@router.get("/", response_model=list[Patient])
def list_patients(db: Session = Depends(get_db)):
    patients = db.query(PatientModel).all()
    return patients

@router.get("/{member_id}", response_model=Patient)
def get_patient(member_id: str, db: Session = Depends(get_db)):
    patient = db.query(PatientModel).filter(PatientModel.member_id == member_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

@router.post("/", response_model=Patient)
def create_patient(patient: PatientBase, db: Session = Depends(get_db)):
    db_patient = PatientModel(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient
