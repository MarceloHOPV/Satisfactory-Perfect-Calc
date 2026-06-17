from __future__ import annotations
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, ConfigDict


# ── Buildings ──────────────────────────────────────────────────────────────────

class BuildingBase(BaseModel):
    name: str
    description: Optional[str] = None

class BuildingCreate(BuildingBase):
    pass

class BuildingUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class BuildingResponse(BuildingBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ── Items ──────────────────────────────────────────────────────────────────────

class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None

class ItemResponse(ItemBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# ── Recipe ingredients / products ─────────────────────────────────────────────

class RecipeIngredientBase(BaseModel):
    item_id: int
    amount_per_min: float

class RecipeProductBase(BaseModel):
    item_id: int
    amount_per_min: float

class RecipeIngredientResponse(RecipeIngredientBase):
    model_config = ConfigDict(from_attributes=True)
    item: ItemResponse

class RecipeProductResponse(RecipeProductBase):
    model_config = ConfigDict(from_attributes=True)
    item: ItemResponse


# ── Recipes ───────────────────────────────────────────────────────────────────

class RecipeBase(BaseModel):
    name: str
    building_id: int
    is_alternate: bool = False

class RecipeCreate(RecipeBase):
    ingredients: List[RecipeIngredientBase]
    products: List[RecipeProductBase]

class RecipeUpdate(BaseModel):
    name: Optional[str] = None
    building_id: Optional[int] = None
    is_alternate: Optional[bool] = None
    ingredients: Optional[List[RecipeIngredientBase]] = None
    products: Optional[List[RecipeProductBase]] = None

class RecipeResponse(RecipeBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    building: BuildingResponse
    ingredients: List[RecipeIngredientResponse]
    products: List[RecipeProductResponse]


# ── Calculator ────────────────────────────────────────────────────────────────

class CalculateRequest(BaseModel):
    target_item_id: int
    target_rate: float
    recipe_overrides: dict[int, int] = {}
    scale_to_integers: bool = False

class ProductionNodeResponse(BaseModel):
    item_id: int
    item_name: str
    rate: float
    is_raw: bool
    recipe_id: Optional[int] = None
    recipe_name: Optional[str] = None
    building_name: Optional[str] = None
    machines: float = 0.0
    inputs: List[ProductionNodeResponse] = []

ProductionNodeResponse.model_rebuild()

class MachineSummaryItem(BaseModel):
    recipe_id: int
    recipe_name: str
    building_name: str
    machines: float

class RawResourceItem(BaseModel):
    item_id: int
    item_name: str
    rate: float

class CalculateResponse(BaseModel):
    tree: ProductionNodeResponse
    machine_summary: List[MachineSummaryItem]
    raw_resources: List[RawResourceItem]
    scale_factor: float = 1.0


# ── Saved productions ─────────────────────────────────────────────────────────

class SavedProductionBase(BaseModel):
    name: str
    description: Optional[str] = None

class SavedProductionCreate(SavedProductionBase):
    config: dict

class SavedProductionUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    config: Optional[dict] = None

class SavedProductionResponse(SavedProductionBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
    config: dict
    created_at: datetime
    updated_at: datetime
