from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database.session import get_db
from app.infrastructure.database.models import Claim as ClaimModel
from app.domain.schemas.schemas import Claim, ClaimBase

router = APIRouter()

@router.get("/", response_model=list[Claim])
def list_claims(db: Session = Depends(get_db)):
    claims = db.query(ClaimModel).all()
    return claims

@router.get("/{claim_id}", response_model=Claim)
def get_claim(claim_id: str, db: Session = Depends(get_db)):
    claim = db.query(ClaimModel).filter(ClaimModel.claim_id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=404, detail="Claim not found")
    return claim

@router.post("/", response_model=Claim)
def create_claim(claim: ClaimBase, db: Session = Depends(get_db)):
    db_claim = ClaimModel(**claim.dict())
    db.add(db_claim)
    db.commit()
    db.refresh(db_claim)
    return db_claim
