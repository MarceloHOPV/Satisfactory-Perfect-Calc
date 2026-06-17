"""
Populates the database with real Satisfactory game data (Update 8).
Safe to run multiple times — skips if data already exists.
"""
import sys
import time
import logging
from sqlalchemy.exc import OperationalError

sys.path.insert(0, "/app")

from app.database import SessionLocal, engine, Base
from app import models

logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
log = logging.getLogger(__name__)

# ── Wait for Postgres ──────────────────────────────────────────────────────────
for attempt in range(15):
    try:
        engine.connect()
        break
    except OperationalError:
        log.info("Waiting for database… (%s/15)", attempt + 1)
        time.sleep(2)
else:
    log.error("Could not connect to the database after 30 s. Exiting.")
    sys.exit(1)

Base.metadata.create_all(bind=engine)
db = SessionLocal()

if db.query(models.Building).count() > 0:
    log.info("Database already seeded — skipping.")
    db.close()
    sys.exit(0)

log.info("Seeding database…")

# ── Buildings ──────────────────────────────────────────────────────────────────
buildings_data = [
    ("Smelter",               "Smelts ore into ingots using 1 ingredient"),
    ("Constructor",           "Constructs basic parts from 1 ingredient"),
    ("Assembler",             "Assembles parts from 2 ingredients"),
    ("Foundry",               "Smelts ore into alloy ingots using 2 ingredients"),
    ("Manufacturer",          "Manufactures complex parts from 3–4 ingredients"),
    ("Oil Refinery",          "Refines crude oil into polymers and fuel"),
    ("Blender",               "Processes up to 4 fluid/solid ingredients"),
    ("Packager",              "Packages or unpackages fluids"),
]
buildings = {}
for name, desc in buildings_data:
    b = models.Building(name=name, description=desc)
    db.add(b)
    db.flush()
    buildings[name] = b

# ── Items ──────────────────────────────────────────────────────────────────────
raw_items = [
    ("Iron Ore",      "Mined from iron deposits"),
    ("Copper Ore",    "Mined from copper deposits"),
    ("Limestone",     "Mined from limestone deposits"),
    ("Coal",          "Mined from coal deposits"),
    ("Caterium Ore",  "Mined from caterium deposits"),
    ("Sulfur",        "Mined from sulfur deposits"),
    ("Raw Quartz",    "Mined from quartz deposits"),
    ("Bauxite",       "Mined from bauxite deposits"),
    ("Uranium",       "Mined from uranium deposits"),
    ("Crude Oil",     "Extracted from oil nodes"),
    ("Water",         "Extracted from water sources"),
]
intermediate_items = [
    ("Iron Ingot",                "Smelted from iron ore"),
    ("Iron Plate",                "Pressed iron ingots"),
    ("Iron Rod",                  "Cast iron rods"),
    ("Screw",                     "Machined screws"),
    ("Reinforced Iron Plate",     "Bolted iron plates"),
    ("Rotor",                     "Assembled rotor"),
    ("Modular Frame",             "Sturdy modular frame"),
    ("Copper Ingot",              "Smelted from copper ore"),
    ("Wire",                      "Drawn copper wire"),
    ("Cable",                     "Bundled wire cable"),
    ("Concrete",                  "Poured concrete"),
    ("Steel Ingot",               "Alloyed steel ingot"),
    ("Steel Beam",                "Hot-rolled steel beam"),
    ("Steel Pipe",                "Extruded steel pipe"),
    ("Encased Industrial Beam",   "Concrete-reinforced steel beam"),
    ("Stator",                    "Electromagnetic stator"),
    ("Motor",                     "Electric motor"),
    ("Copper Sheet",              "Rolled copper sheet"),
    ("Versatile Framework",       "Modular steel framework"),
    ("Caterium Ingot",            "Smelted from caterium ore"),
    ("Quickwire",                 "High-speed caterium wire"),
    ("Silica",                    "Refined quartz silica"),
    ("Quartz Crystal",            "Refined quartz crystal"),
    ("Plastic",                   "Polymer plastic"),
    ("Rubber",                    "Polymer rubber"),
    ("Fuel",                      "Liquid fuel"),
    ("Circuit Board",             "Printed circuit board"),
    ("Computer",                  "High-performance computer"),
    ("AI Limiter",                "Caterium AI limiter"),
    ("High-Speed Connector",      "High-frequency connector"),
]

items: dict[str, models.Item] = {}

for name, desc in raw_items:
    it = models.Item(name=name, description=desc, category="raw")
    db.add(it)
    db.flush()
    items[name] = it

for name, desc in intermediate_items:
    it = models.Item(name=name, description=desc, category="intermediate")
    db.add(it)
    db.flush()
    items[name] = it

# ── Helper ─────────────────────────────────────────────────────────────────────

def add_recipe(name, building_name, ingredients, products, alternate=False):
    """
    ingredients / products: list of (item_name, amount_per_min)
    """
    recipe = models.Recipe(
        name=name,
        building_id=buildings[building_name].id,
        is_alternate=alternate,
    )
    db.add(recipe)
    db.flush()
    for item_name, rate in ingredients:
        db.add(models.RecipeIngredient(
            recipe_id=recipe.id,
            item_id=items[item_name].id,
            amount_per_min=rate,
        ))
    for item_name, rate in products:
        db.add(models.RecipeProduct(
            recipe_id=recipe.id,
            item_id=items[item_name].id,
            amount_per_min=rate,
        ))
    return recipe

# ── Recipes ─────────────────────────────────────────────────────────────────────
# All rates are per-minute at 100 % clock speed (Update 8 values)

# Phase 1
add_recipe("Iron Ingot",
    "Smelter",
    [("Iron Ore", 30)],
    [("Iron Ingot", 30)])

add_recipe("Iron Plate",
    "Constructor",
    [("Iron Ingot", 30)],
    [("Iron Plate", 20)])

add_recipe("Iron Rod",
    "Constructor",
    [("Iron Ingot", 15)],
    [("Iron Rod", 15)])

add_recipe("Screw",
    "Constructor",
    [("Iron Rod", 10)],
    [("Screw", 40)])

add_recipe("Reinforced Iron Plate",
    "Assembler",
    [("Iron Plate", 30), ("Screw", 60)],
    [("Reinforced Iron Plate", 5)])

add_recipe("Rotor",
    "Assembler",
    [("Iron Rod", 20), ("Screw", 100)],
    [("Rotor", 4)])

add_recipe("Modular Frame",
    "Assembler",
    [("Reinforced Iron Plate", 3), ("Iron Rod", 12)],
    [("Modular Frame", 2)])

add_recipe("Copper Ingot",
    "Smelter",
    [("Copper Ore", 30)],
    [("Copper Ingot", 30)])

add_recipe("Wire",
    "Constructor",
    [("Copper Ingot", 15)],
    [("Wire", 30)])

add_recipe("Cable",
    "Constructor",
    [("Wire", 60)],
    [("Cable", 30)])

add_recipe("Concrete",
    "Constructor",
    [("Limestone", 45)],
    [("Concrete", 15)])

add_recipe("Copper Sheet",
    "Constructor",
    [("Copper Ingot", 20)],
    [("Copper Sheet", 10)])

# Phase 2
add_recipe("Steel Ingot",
    "Foundry",
    [("Iron Ore", 45), ("Coal", 45)],
    [("Steel Ingot", 45)])

add_recipe("Steel Beam",
    "Constructor",
    [("Steel Ingot", 60)],
    [("Steel Beam", 15)])

add_recipe("Steel Pipe",
    "Constructor",
    [("Steel Ingot", 30)],
    [("Steel Pipe", 20)])

add_recipe("Encased Industrial Beam",
    "Assembler",
    [("Steel Beam", 24), ("Concrete", 30)],
    [("Encased Industrial Beam", 6)])

add_recipe("Stator",
    "Assembler",
    [("Steel Pipe", 15), ("Wire", 40)],
    [("Stator", 5)])

add_recipe("Motor",
    "Assembler",
    [("Rotor", 10), ("Stator", 10)],
    [("Motor", 5)])

add_recipe("Versatile Framework",
    "Assembler",
    [("Modular Frame", 2.5), ("Steel Beam", 30)],
    [("Versatile Framework", 5)])

# Phase 3
add_recipe("Caterium Ingot",
    "Smelter",
    [("Caterium Ore", 45)],
    [("Caterium Ingot", 15)])

add_recipe("Quickwire",
    "Constructor",
    [("Caterium Ingot", 12)],
    [("Quickwire", 60)])

add_recipe("Silica",
    "Constructor",
    [("Raw Quartz", 22.5)],
    [("Silica", 37.5)])

add_recipe("Quartz Crystal",
    "Constructor",
    [("Raw Quartz", 37.5)],
    [("Quartz Crystal", 22.5)])

add_recipe("AI Limiter",
    "Assembler",
    [("Copper Sheet", 25), ("Quickwire", 100)],
    [("AI Limiter", 5)])

add_recipe("Plastic",
    "Oil Refinery",
    [("Crude Oil", 30)],
    [("Plastic", 20), ("Fuel", 10)])

add_recipe("Rubber",
    "Oil Refinery",
    [("Crude Oil", 30)],
    [("Rubber", 20), ("Fuel", 20)])

add_recipe("Circuit Board",
    "Assembler",
    [("Copper Sheet", 15), ("Plastic", 30)],
    [("Circuit Board", 7.5)])

add_recipe("High-Speed Connector",
    "Manufacturer",
    [("Quickwire", 210), ("Cable", 37.5), ("Circuit Board", 3.75)],
    [("High-Speed Connector", 3.75)])

add_recipe("Computer",
    "Manufacturer",
    [("Circuit Board", 25), ("Cable", 22.5), ("Plastic", 45), ("Screw", 130)],
    [("Computer", 2.5)])

# ── Alternate recipes (examples) ──────────────────────────────────────────────
add_recipe("Alternate: Stitched Iron Plate",
    "Assembler",
    [("Iron Plate", 18.75), ("Wire", 37.5)],
    [("Reinforced Iron Plate", 5.625)],
    alternate=True)

add_recipe("Alternate: Steel Screw",
    "Constructor",
    [("Steel Beam", 5)],
    [("Screw", 260)],
    alternate=True)

add_recipe("Alternate: Caterium Wire",
    "Constructor",
    [("Caterium Ingot", 15)],
    [("Wire", 120)],
    alternate=True)

db.commit()
log.info("Seed complete: %d buildings, %d items, %d recipes.",
         db.query(models.Building).count(),
         db.query(models.Item).count(),
         db.query(models.Recipe).count())
db.close()
