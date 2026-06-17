from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from .. import models, schemas
from ..services import calculator as calc_service

router = APIRouter(prefix="/calculate", tags=["calculator"])


@router.post("/", response_model=schemas.CalculateResponse)
def calculate_production(
    payload: schemas.CalculateRequest,
    db: Session = Depends(get_db),
):
    if not db.query(models.Item).filter(models.Item.id == payload.target_item_id).first():
        raise HTTPException(status_code=404, detail="Target item not found")
    if payload.target_rate <= 0:
        raise HTTPException(status_code=400, detail="target_rate must be positive")

    try:
        result = calc_service.calculate(
            db=db,
            target_item_id=payload.target_item_id,
            target_rate=payload.target_rate,
            recipe_overrides=payload.recipe_overrides,
            scale_to_integers=payload.scale_to_integers,
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    return result
