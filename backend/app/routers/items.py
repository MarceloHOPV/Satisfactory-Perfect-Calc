from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/items", tags=["items"])


@router.get("/", response_model=List[schemas.ItemResponse])
def list_items(
    category: Optional[str] = Query(None),
    search: Optional[str] = Query(None),
    db: Session = Depends(get_db),
):
    q = db.query(models.Item)
    if category:
        q = q.filter(models.Item.category == category)
    if search:
        q = q.filter(models.Item.name.ilike(f"%{search}%"))
    return q.order_by(models.Item.name).all()


@router.get("/{item_id}", response_model=schemas.ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@router.post("/", response_model=schemas.ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: schemas.ItemCreate, db: Session = Depends(get_db)):
    if db.query(models.Item).filter(models.Item.name == payload.name).first():
        raise HTTPException(status_code=400, detail="Item name already exists")
    item = models.Item(**payload.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.put("/{item_id}", response_model=schemas.ItemResponse)
def update_item(
    item_id: int,
    payload: schemas.ItemUpdate,
    db: Session = Depends(get_db),
):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
