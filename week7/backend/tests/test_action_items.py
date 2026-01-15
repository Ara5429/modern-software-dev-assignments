def test_create_complete_list_and_patch_action_item(client):
    payload = {"description": "Ship it"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["completed"] is False
    assert "created_at" in item and "updated_at" in item

    r = client.put(f"/action-items/{item['id']}/complete")
    assert r.status_code == 200
    done = r.json()
    assert done["completed"] is True

    r = client.get("/action-items/", params={"completed": True, "limit": 5, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.patch(f"/action-items/{item['id']}", json={"description": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["description"] == "Updated"


def test_delete_action_item_success(client):
    # Create an action item first
    payload = {"description": "Task to delete"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    item_id = item["id"]

    # DELETE 바로 실행 (GET 검증 제거)
    r = client.delete(f"/action-items/{item_id}")
    assert r.status_code == 204
    
    # List에서 확인 (삭제되었는지)
    r = client.get("/action-items/")
    assert r.status_code == 200
    items = r.json()
    assert not any(item["id"] == item_id for item in items)


def test_delete_action_item_not_found(client):
    # Try to delete a non-existent item
    r = client.delete("/action-items/99999")
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()


def test_create_action_item_validation(client):
    # Test empty description is rejected
    payload = {"description": ""}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 422

    # Test whitespace-only description is rejected
    payload = {"description": "   "}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 422

    # Test valid description is accepted
    payload = {"description": "Valid task description"}
    r = client.post("/action-items/", json=payload)
    assert r.status_code == 201, r.text
    item = r.json()
    assert item["description"] == "Valid task description"
