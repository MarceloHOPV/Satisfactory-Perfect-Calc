from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .. import models, schemas

router = APIRouter(prefix="/recipes", tags=["recipes"])


@router.get("/", response_model=List[schemas.RecipeResponse])
def list_recipes(
    building_id: Optional[int] = Query(None),
    item_id: Optional[int] = Query(None, description="Filter by produced item"),
    include_alternates: bool = Query(True),
    db: Session = Depends(get_db),
):
    q = db.query(models.Recipe)
    if building_id:
        q = q.filter(models.Recipe.building_id == building_id)
    if not include_alternates:
        q = q.filter(models.Recipe.is_alternate == False)
    if item_id:
        q = q.join(models.RecipeProduct).filter(
            models.RecipeProduct.item_id == item_id
        )
    return q.all()


@router.get("/{recipe_id}", response_model=schemas.RecipeResponse)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe


@router.post("/", response_model=schemas.RecipeResponse, status_code=status.HTTP_201_CREATED)
def create_recipe(payload: schemas.RecipeCreate, db: Session = Depends(get_db)):
    if not db.query(models.Building).filter(models.Building.id == payload.building_id).first():
        raise HTTPException(status_code=404, detail="Building not found")

    recipe = models.Recipe(
        name=payload.name,
        building_id=payload.building_id,
        is_alternate=payload.is_alternate,
    )
    db.add(recipe)
    db.flush()  # get recipe.id before adding children

    for ing in payload.ingredients:
        if not db.query(models.Item).filter(models.Item.id == ing.item_id).first():
            raise HTTPException(status_code=404, detail=f"Item id={ing.item_id} not found")
        db.add(models.RecipeIngredient(
            recipe_id=recipe.id,
            item_id=ing.item_id,
            amount_per_min=ing.amount_per_min,
        ))

    for prod in payload.products:
        if not db.query(models.Item).filter(models.Item.id == prod.item_id).first():
            raise HTTPException(status_code=404, detail=f"Item id={prod.item_id} not found")
        db.add(models.RecipeProduct(
            recipe_id=recipe.id,
            item_id=prod.item_id,
            amount_per_min=prod.amount_per_min,
        ))

    db.commit()
    db.refresh(recipe)
    return recipe


@router.put("/{recipe_id}", response_model=schemas.RecipeResponse)
def update_recipe(
    recipe_id: int,
    payload: schemas.RecipeUpdate,
    db: Session = Depends(get_db),
):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    for field in ("name", "building_id", "is_alternate"):
        value = getattr(payload, field)
        if value is not None:
            setattr(recipe, field, value)

    if payload.ingredients is not None:
        db.query(models.RecipeIngredient).filter(
            models.RecipeIngredient.recipe_id == recipe_id
        ).delete()
        for ing in payload.ingredients:
            db.add(models.RecipeIngredient(
                recipe_id=recipe_id,
                item_id=ing.item_id,
                amount_per_min=ing.amount_per_min,
            ))

    if payload.products is not None:
        db.query(models.RecipeProduct).filter(
            models.RecipeProduct.recipe_id == recipe_id
        ).delete()
        for prod in payload.products:
            db.add(models.RecipeProduct(
                recipe_id=recipe_id,
                item_id=prod.item_id,
                amount_per_min=prod.amount_per_min,
            ))

    db.commit()
    db.refresh(recipe)
    return recipe


@router.delete("/{recipe_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(recipe)
    db.commit()
