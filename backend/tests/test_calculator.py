"""Calculator endpoint tests using a small fixture production chain:

  Iron Ore (raw)
      └─ Iron Ingot  (Smelter, 30 ore → 30 ingot)
          ├─ Iron Plate  (Constructor, 30 ingot → 20 plates)
          └─ Iron Rod    (Constructor, 15 ingot → 15 rods)
                └─ Screw (Constructor, 10 rods → 40 screws)
"""
import pytest
from .conftest import make_building, make_item, make_recipe


def _setup_chain(db):
    smelter     = make_building(db, "Smelter")
    constructor = make_building(db, "Constructor")

    iron_ore   = make_item(db, "Iron Ore",   "raw")
    iron_ingot = make_item(db, "Iron Ingot", "intermediate")
    iron_plate = make_item(db, "Iron Plate", "intermediate")
    iron_rod   = make_item(db, "Iron Rod",   "intermediate")
    screw      = make_item(db, "Screw",      "intermediate")

    make_recipe(db, "Iron Ingot", smelter.id,     [(iron_ore.id, 30)],   [(iron_ingot.id, 30)])
    make_recipe(db, "Iron Plate", constructor.id, [(iron_ingot.id, 30)], [(iron_plate.id, 20)])
    make_recipe(db, "Iron Rod",   constructor.id, [(iron_ingot.id, 15)], [(iron_rod.id, 15)])
    make_recipe(db, "Screw",      constructor.id, [(iron_rod.id, 10)],   [(screw.id, 40)])

    return dict(
        iron_ore=iron_ore, iron_ingot=iron_ingot,
        iron_plate=iron_plate, iron_rod=iron_rod, screw=screw,
    )


def test_calculate_iron_plate(client, db):
    chain = _setup_chain(db)
    res = client.post("/api/v1/calculate/", json={
        "target_item_id": chain["iron_plate"].id,
        "target_rate": 20.0,
    })
    assert res.status_code == 200
    data = res.json()
    assert data["tree"]["item_id"] == chain["iron_plate"].id
    assert data["tree"]["machines"] == pytest.approx(1.0)
    raw = {r["item_id"]: r["rate"] for r in data["raw_resources"]}
    assert raw[chain["iron_ore"].id] == pytest.approx(30.0)


def test_calculate_screw_chain(client, db):
    chain = _setup_chain(db)
    res = client.post("/api/v1/calculate/", json={
        "target_item_id": chain["screw"].id,
        "target_rate": 40.0,
    })
    assert res.status_code == 200
    machines = {m["recipe_name"]: m["machines"] for m in res.json()["machine_summary"]}
    assert machines["Screw"]      == pytest.approx(1.0)
    assert machines["Iron Rod"]   == pytest.approx(2 / 3)
    assert machines["Iron Ingot"] == pytest.approx(1 / 3)


def test_calculate_scale_to_integers(client, db):
    chain = _setup_chain(db)
    res = client.post("/api/v1/calculate/", json={
        "target_item_id": chain["screw"].id,
        "target_rate": 10.0,
        "scale_to_integers": True,
    })
    assert res.status_code == 200
    data = res.json()
    for m in data["machine_summary"]:
        assert float(m["machines"]).is_integer(), f"{m['recipe_name']} has fractional machines"
    assert data["scale_factor"] >= 1.0


def test_calculate_item_not_found(client):
    res = client.post("/api/v1/calculate/", json={
        "target_item_id": 9999,
        "target_rate": 60.0,
    })
    assert res.status_code == 404


def test_calculate_raw_resource_directly(client, db):
    chain = _setup_chain(db)
    res = client.post("/api/v1/calculate/", json={
        "target_item_id": chain["iron_ore"].id,
        "target_rate": 60.0,
    })
    assert res.status_code == 200
    data = res.json()
    assert data["tree"]["is_raw"] is True
    assert data["machine_summary"] == []
