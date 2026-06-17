from .conftest import make_item


def test_create_item(client):
    res = client.post("/api/v1/items/", json={"name": "Iron Ore", "category": "raw"})
    assert res.status_code == 201
    data = res.json()
    assert data["name"] == "Iron Ore"
    assert data["category"] == "raw"
    assert "id" in data


def test_create_duplicate_item(client, db):
    make_item(db, "Iron Ore")
    res = client.post("/api/v1/items/", json={"name": "Iron Ore"})
    assert res.status_code == 400


def test_list_items(client, db):
    make_item(db, "Iron Ore")
    make_item(db, "Copper Ore")
    res = client.get("/api/v1/items/")
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_list_items_search(client, db):
    make_item(db, "Iron Ore")
    make_item(db, "Copper Ore")
    res = client.get("/api/v1/items/?search=iron")
    assert res.status_code == 200
    names = [i["name"] for i in res.json()]
    assert "Iron Ore" in names
    assert "Copper Ore" not in names


def test_get_item(client, db):
    item = make_item(db)
    res = client.get(f"/api/v1/items/{item.id}")
    assert res.status_code == 200
    assert res.json()["id"] == item.id


def test_get_item_not_found(client):
    res = client.get("/api/v1/items/9999")
    assert res.status_code == 404


def test_update_item(client, db):
    item = make_item(db)
    res = client.put(f"/api/v1/items/{item.id}", json={"category": "intermediate"})
    assert res.status_code == 200
    assert res.json()["category"] == "intermediate"


def test_delete_item(client, db):
    item = make_item(db)
    res = client.delete(f"/api/v1/items/{item.id}")
    assert res.status_code == 204
    assert client.get(f"/api/v1/items/{item.id}").status_code == 404
