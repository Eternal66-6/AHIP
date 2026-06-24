from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.infrastructure.database.session import get_db
from app.infrastructure.database.models import Provider as ProviderModel
from app.domain.schemas.schemas import Provider, ProviderBase

router = APIRouter()

@router.get("/", response_model=list[Provider])
def list_providers(db: Session = Depends(get_db)):
    providers = db.query(ProviderModel).all()
    return providers

@router.get("/{provider_id}", response_model=Provider)
def get_provider(provider_id: str, db: Session = Depends(get_db)):
    provider = db.query(ProviderModel).filter(ProviderModel.provider_id == provider_id).first()
    if not provider:
        raise HTTPException(status_code=404, detail="Provider not found")
    return provider

@router.post("/", response_model=Provider)
def create_provider(provider: ProviderBase, db: Session = Depends(get_db)):
    db_provider = ProviderModel(**provider.dict())
    db.add(db_provider)
    db.commit()
    db.refresh(db_provider)
    return db_provider
