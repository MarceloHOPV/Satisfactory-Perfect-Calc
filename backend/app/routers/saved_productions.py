from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/saved-productions", tags=["saved-productions"])


@router.get("/", response_model=List[schemas.SavedProductionResponse])
def list_saved(db: Session = Depends(get_db)):
    return (
        db.query(models.SavedProduction)
        .order_by(models.SavedProduction.updated_at.desc())
        .all()
    )


@router.get("/{prod_id}", response_model=schemas.SavedProductionResponse)
def get_saved(prod_id: int, db: Session = Depends(get_db)):
    sp = db.query(models.SavedProduction).filter(models.SavedProduction.id == prod_id).first()
    if not sp:
        raise HTTPException(status_code=404, detail="Saved production not found")
    return sp


@router.post("/", response_model=schemas.SavedProductionResponse, status_code=status.HTTP_201_CREATED)
def create_saved(payload: schemas.SavedProductionCreate, db: Session = Depends(get_db)):
    sp = models.SavedProduction(**payload.model_dump())
    db.add(sp)
    db.commit()
    db.refresh(sp)
    return sp


@router.put("/{prod_id}", response_model=schemas.SavedProductionResponse)
def update_saved(
    prod_id: int,
    payload: schemas.SavedProductionUpdate,
    db: Session = Depends(get_db),
):
    sp = db.query(models.SavedProduction).filter(models.SavedProduction.id == prod_id).first()
    if not sp:
        raise HTTPException(status_code=404, detail="Saved production not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(sp, field, value)
    sp.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(sp)
    return sp


@router.delete("/{prod_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_saved(prod_id: int, db: Session = Depends(get_db)):
    sp = db.query(models.SavedProduction).filter(models.SavedProduction.id == prod_id).first()
    if not sp:
        raise HTTPException(status_code=404, detail="Saved production not found")
    db.delete(sp)
    db.commit()
