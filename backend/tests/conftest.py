import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.database import Base, get_db
from app import models

SQLALCHEMY_TEST_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_TEST_URL, connect_args={"check_same_thread": False}
)
TestingSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSession()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def db():
    session = TestingSession()
    try:
        yield session
    finally:
        session.close()


# ── Helpers ────────────────────────────────────────────────────────────────────

def make_building(db, name="Smelter"):
    b = models.Building(name=name)
    db.add(b)
    db.commit()
    db.refresh(b)
    return b


def make_item(db, name="Iron Ore", category="raw"):
    it = models.Item(name=name, category=category)
    db.add(it)
    db.commit()
    db.refresh(it)
    return it


def make_recipe(db, name, building_id, ingredients, products, is_alternate=False):
    recipe = models.Recipe(name=name, building_id=building_id, is_alternate=is_alternate)
    db.add(recipe)
    db.flush()
    for item_id, rate in ingredients:
        db.add(models.RecipeIngredient(recipe_id=recipe.id, item_id=item_id, amount_per_min=rate))
    for item_id, rate in products:
        db.add(models.RecipeProduct(recipe_id=recipe.id, item_id=item_id, amount_per_min=rate))
    db.commit()
    db.refresh(recipe)
    return recipe
