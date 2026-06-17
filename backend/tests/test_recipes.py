from .conftest import make_building, make_item, make_recipe


def test_create_recipe(client, db):
    b = make_building(db)
    ore = make_item(db, "Iron Ore")
    ingot = make_item(db, "Iron Ingot", "intermediate")

    res = client.post("/api/v1/recipes/", json={
        "name": "Iron Ingot",
        "building_id": b.id,
        "is_alternate": False,
        "ingredients": [{"item_id": ore.id, "amount_per_min": 30}],
        "products": [{"item_id": ingot.id, "amount_per_min": 30}],
    })
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Iron Ingot"
    assert len(data["ingredients"]) == 1
    assert len(data["products"]) == 1


def test_get_recipe(client, db):
    b = make_building(db)
    ore = make_item(db, "Iron Ore")
    ingot = make_item(db, "Iron Ingot", "intermediate")
    recipe = make_recipe(db, "Iron Ingot", b.id, [(ore.id, 30)], [(ingot.id, 30)])

    res = client.get(f"/api/v1/recipes/{recipe.id}")
    assert res.status_code == 200
    assert res.json()["id"] == recipe.id


def test_list_recipes_filter_by_item(client, db):
    b = make_building(db)
    ore = make_item(db, "Iron Ore")
    ingot = make_item(db, "Iron Ingot", "intermediate")
    plate = make_item(db, "Iron Plate", "intermediate")
    make_recipe(db, "Iron Ingot", b.id, [(ore.id, 30)], [(ingot.id, 30)])
    make_recipe(db, "Iron Plate", b.id, [(ingot.id, 30)], [(plate.id, 20)])

    res = client.get(f"/api/v1/recipes/?item_id={plate.id}")
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["name"] == "Iron Plate"


def test_update_recipe(client, db):
    b = make_building(db)
    ore = make_item(db, "Iron Ore")
    ingot = make_item(db, "Iron Ingot", "intermediate")
    recipe = make_recipe(db, "Iron Ingot", b.id, [(ore.id, 30)], [(ingot.id, 30)])

    res = client.put(f"/api/v1/recipes/{recipe.id}", json={"name": "Iron Ingot (Updated)"})
    assert res.status_code == 200
    assert res.json()["name"] == "Iron Ingot (Updated)"


def test_delete_recipe(client, db):
    b = make_building(db)
    ore = make_item(db, "Iron Ore")
    ingot = make_item(db, "Iron Ingot", "intermediate")
    recipe = make_recipe(db, "Iron Ingot", b.id, [(ore.id, 30)], [(ingot.id, 30)])

    res = client.delete(f"/api/v1/recipes/{recipe.id}")
    assert res.status_code == 204
    assert client.get(f"/api/v1/recipes/{recipe.id}").status_code == 404
