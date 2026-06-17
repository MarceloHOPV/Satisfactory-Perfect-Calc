from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/buildings", tags=["buildings"])


@router.get("/", response_model=List[schemas.BuildingResponse])
def list_buildings(db: Session = Depends(get_db)):
    return db.query(models.Building).all()


@router.get("/{building_id}", response_model=schemas.BuildingResponse)
def get_building(building_id: int, db: Session = Depends(get_db)):
    building = db.query(models.Building).filter(models.Building.id == building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    return building


@router.post("/", response_model=schemas.BuildingResponse, status_code=status.HTTP_201_CREATED)
def create_building(payload: schemas.BuildingCreate, db: Session = Depends(get_db)):
    if db.query(models.Building).filter(models.Building.name == payload.name).first():
        raise HTTPException(status_code=400, detail="Building name already exists")
    building = models.Building(**payload.model_dump())
    db.add(building)
    db.commit()
    db.refresh(building)
    return building


@router.put("/{building_id}", response_model=schemas.BuildingResponse)
def update_building(
    building_id: int,
    payload: schemas.BuildingUpdate,
    db: Session = Depends(get_db),
):
    building = db.query(models.Building).filter(models.Building.id == building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(building, field, value)
    db.commit()
    db.refresh(building)
    return building


@router.delete("/{building_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_building(building_id: int, db: Session = Depends(get_db)):
    building = db.query(models.Building).filter(models.Building.id == building_id).first()
    if not building:
        raise HTTPException(status_code=404, detail="Building not found")
    db.delete(building)
    db.commit()
