from sqlalchemy import Column, Integer, String, Float, Boolean, Text, ForeignKey, DateTime, JSON
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class Building(Base):
    __tablename__ = "buildings"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)

    # 1:N — a building hosts many recipes
    recipes = relationship("Recipe", back_populates="building")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    # "raw", "intermediate", "component", "equipment"
    category = Column(String(50), nullable=True)

    # N:M via junction tables
    as_ingredient = relationship("RecipeIngredient", back_populates="item")
    as_product = relationship("RecipeProduct", back_populates="item")


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    # N:1 — many recipes belong to one building
    building_id = Column(Integer, ForeignKey("buildings.id"), nullable=False)
    is_alternate = Column(Boolean, default=False, nullable=False)

    building = relationship("Building", back_populates="recipes")
    # N:M → items (inputs)  — cascade keeps junction rows consistent
    ingredients = relationship(
        "RecipeIngredient", back_populates="recipe", cascade="all, delete-orphan"
    )
    # N:M → items (outputs)
    products = relationship(
        "RecipeProduct", back_populates="recipe", cascade="all, delete-orphan"
    )


class RecipeIngredient(Base):
    """Junction: Recipe ↔ Item as input (N:M)."""
    __tablename__ = "recipe_ingredients"

    recipe_id = Column(
        Integer, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True
    )
    item_id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    amount_per_min = Column(Float, nullable=False)

    recipe = relationship("Recipe", back_populates="ingredients")
    item = relationship("Item", back_populates="as_ingredient")


class RecipeProduct(Base):
    """Junction: Recipe ↔ Item as output (N:M)."""
    __tablename__ = "recipe_products"

    recipe_id = Column(
        Integer, ForeignKey("recipes.id", ondelete="CASCADE"), primary_key=True
    )
    item_id = Column(Integer, ForeignKey("items.id"), primary_key=True)
    amount_per_min = Column(Float, nullable=False)

    recipe = relationship("Recipe", back_populates="products")
    item = relationship("Item", back_populates="as_product")


class SavedProduction(Base):
    __tablename__ = "saved_productions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    config = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
