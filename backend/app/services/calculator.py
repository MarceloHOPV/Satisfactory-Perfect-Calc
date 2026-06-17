from __future__ import annotations
from math import gcd
from fractions import Fraction
from functools import reduce
from typing import Optional
from sqlalchemy.orm import Session

from .. import models


def _lcm(a: int, b: int) -> int:
    return a * b // gcd(a, b)


def _get_recipe(
    db: Session,
    item_id: int,
    overrides: dict[int, int],
) -> Optional[models.Recipe]:
    """Return the preferred recipe that produces `item_id`."""
    if item_id in overrides:
        rp = (
            db.query(models.RecipeProduct)
            .filter(
                models.RecipeProduct.recipe_id == overrides[item_id],
                models.RecipeProduct.item_id == item_id,
            )
            .first()
        )
        if rp:
            return rp.recipe

    # Prefer standard (non-alternate) recipes
    rp = (
        db.query(models.RecipeProduct)
        .join(models.Recipe)
        .filter(models.RecipeProduct.item_id == item_id)
        .order_by(models.Recipe.is_alternate)
        .first()
    )
    return rp.recipe if rp else None


def _scale_node(node: dict, factor: float) -> dict:
    return {
        **node,
        "rate": node["rate"] * factor,
        "machines": node["machines"] * factor,
        "inputs": [_scale_node(child, factor) for child in node["inputs"]],
    }


def calculate(
    db: Session,
    target_item_id: int,
    target_rate: float,
    recipe_overrides: dict[int, int],
    scale_to_integers: bool,
) -> dict:
    """
    Recursively resolve the production tree for the target item.

    The algorithm walks the dependency DAG depth-first, accumulating
    machine counts and raw-resource demand in shared dicts so that
    items consumed by multiple branches are summed correctly in the
    summary (while the tree shows the full decomposition per branch).
    """
    machine_demands: dict[int, float] = {}   # recipe_id → total machines
    raw_demands: dict[int, float] = {}        # item_id  → rate /min
    recipe_cache: dict[int, models.Recipe] = {}
    item_cache: dict[int, models.Item] = {}

    def _item(item_id: int) -> models.Item:
        if item_id not in item_cache:
            item_cache[item_id] = (
                db.query(models.Item).filter(models.Item.id == item_id).first()
            )
        return item_cache[item_id]

    def resolve(item_id: int, needed_rate: float) -> dict:
        item = _item(item_id)
        if item is None:
            raise ValueError(f"Item id={item_id} not found")

        recipe = _get_recipe(db, item_id, recipe_overrides)

        if recipe is None:
            # Base case: raw resource — no manufacturing recipe
            raw_demands[item_id] = raw_demands.get(item_id, 0.0) + needed_rate
            return {
                "item_id": item_id,
                "item_name": item.name,
                "rate": needed_rate,
                "is_raw": True,
                "recipe_id": None,
                "recipe_name": None,
                "building_name": None,
                "machines": 0.0,
                "inputs": [],
            }

        product_entry = next(
            (p for p in recipe.products if p.item_id == item_id), None
        )
        if product_entry is None:
            raise ValueError(
                f"Recipe id={recipe.id} does not list item id={item_id} as a product"
            )

        machines_needed = needed_rate / product_entry.amount_per_min
        machine_demands[recipe.id] = (
            machine_demands.get(recipe.id, 0.0) + machines_needed
        )
        recipe_cache[recipe.id] = recipe

        inputs = [
            resolve(ing.item_id, ing.amount_per_min * machines_needed)
            for ing in recipe.ingredients
        ]

        return {
            "item_id": item_id,
            "item_name": item.name,
            "rate": needed_rate,
            "is_raw": False,
            "recipe_id": recipe.id,
            "recipe_name": recipe.name,
            "building_name": recipe.building.name,
            "machines": machines_needed,
            "inputs": inputs,
        }

    tree = resolve(target_item_id, target_rate)

    machine_summary = [
        {
            "recipe_id": rid,
            "recipe_name": recipe_cache[rid].name,
            "building_name": recipe_cache[rid].building.name,
            "machines": count,
        }
        for rid, count in machine_demands.items()
    ]

    raw_resources = [
        {"item_id": iid, "item_name": _item(iid).name, "rate": rate}
        for iid, rate in raw_demands.items()
    ]

    scale_factor = 1.0

    if scale_to_integers and machine_demands:
        # Find LCM of all machine-count denominators to get integer machines
        fracs = [
            Fraction(v).limit_denominator(10_000)
            for v in machine_demands.values()
        ]
        denominators = [f.denominator for f in fracs]
        lcm_val = reduce(_lcm, denominators)
        scale_factor = float(lcm_val)

        tree = _scale_node(tree, scale_factor)
        machine_summary = [
            {**m, "machines": round(m["machines"] * scale_factor)}
            for m in machine_summary
        ]
        raw_resources = [
            {**r, "rate": r["rate"] * scale_factor}
            for r in raw_resources
        ]

    return {
        "tree": tree,
        "machine_summary": machine_summary,
        "raw_resources": raw_resources,
        "scale_factor": scale_factor,
    }
