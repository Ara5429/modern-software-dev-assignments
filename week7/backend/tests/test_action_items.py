import time

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


def test_pagination_action_items_basic(client):
    # Create 10 items with time delays
    item_ids = []
    for i in range(10):
        payload = {"description": f"Task {i}"}
        r = client.post("/action-items/", json=payload)
        assert r.status_code == 201, f"Failed to create item {i}: {r.text}"
        item_ids.append(r.json()["id"])
        time.sleep(0.01)
    
    # Test skip=0, limit=5 returns 5 items
    r = client.get("/action-items/", params={"skip": 0, "limit": 5})
    assert r.status_code == 200, f"Failed to get first page: {r.text}"
    first_page = r.json()
    assert len(first_page) == 5, f"Expected 5 items, got {len(first_page)}"
    first_page_ids = [item["id"] for item in first_page]
    
    # Test skip=5, limit=5 returns next 5
    r = client.get("/action-items/", params={"skip": 5, "limit": 5})
    assert r.status_code == 200, f"Failed to get second page: {r.text}"
    second_page = r.json()
    assert len(second_page) == 5, f"Expected 5 items, got {len(second_page)}"
    second_page_ids = [item["id"] for item in second_page]
    
    # Verify both sets are different
    assert set(first_page_ids) != set(second_page_ids), "First and second page should have different items"


def test_pagination_edge_cases(client):
    # Create 5 items
    for i in range(5):
        payload = {"description": f"Task {i}"}
        r = client.post("/action-items/", json=payload)
        assert r.status_code == 201, f"Failed to create item {i}: {r.text}"
        time.sleep(0.01)
    
    # Test skip=100 returns empty list
    r = client.get("/action-items/", params={"skip": 100})
    assert r.status_code == 200, f"Failed to get items with skip=100: {r.text}"
    items = r.json()
    assert len(items) == 0, f"Expected empty list, got {len(items)} items"
    
    # Test limit=1 returns exactly 1
    r = client.get("/action-items/", params={"limit": 1})
    assert r.status_code == 200, f"Failed to get items with limit=1: {r.text}"
    items = r.json()
    assert len(items) == 1, f"Expected 1 item, got {len(items)}"
    
    # Test limit=200 returns all (max allowed)
    r = client.get("/action-items/", params={"limit": 200})
    assert r.status_code == 200, f"Failed to get items with limit=200: {r.text}"
    items = r.json()
    assert len(items) >= 5, f"Expected at least 5 items, got {len(items)}"


def test_sorting_by_created_at(client):
    # Create 3 items with time.sleep(0.01) between each
    item_ids = []
    for i in range(3):
        payload = {"description": f"Task {i}"}
        r = client.post("/action-items/", json=payload)
        assert r.status_code == 201, f"Failed to create item {i}: {r.text}"
        item_ids.append(r.json()["id"])
        time.sleep(0.01)
    
    # Test sort="-created_at" returns newest first (last ID first)
    r = client.get("/action-items/", params={"sort": "-created_at", "limit": 10})
    assert r.status_code == 200, f"Failed to get items sorted by -created_at: {r.text}"
    items_desc = r.json()
    assert len(items_desc) >= 3, f"Expected at least 3 items, got {len(items_desc)}"
    # The last created item (last in item_ids) should be first in the sorted list
    assert items_desc[0]["id"] == item_ids[-1], f"Expected newest item {item_ids[-1]} first, got {items_desc[0]['id']}"
    
    # Test sort="created_at" returns oldest first (first ID first)
    r = client.get("/action-items/", params={"sort": "created_at", "limit": 10})
    assert r.status_code == 200, f"Failed to get items sorted by created_at: {r.text}"
    items_asc = r.json()
    assert len(items_asc) >= 3, f"Expected at least 3 items, got {len(items_asc)}"
    # The first created item (first in item_ids) should be first in the sorted list
    # Note: We need to find our items in the list since there might be other items
    found_ids = [item["id"] for item in items_asc if item["id"] in item_ids]
    assert found_ids[0] == item_ids[0], f"Expected oldest item {item_ids[0]} first, got {found_ids[0] if found_ids else 'none'}"


def test_pagination_with_completed_filter(client):
    # Create 10 items
    item_ids = []
    for i in range(10):
        payload = {"description": f"Task {i}"}
        r = client.post("/action-items/", json=payload)
        assert r.status_code == 201, f"Failed to create item {i}: {r.text}"
        item_ids.append(r.json()["id"])
        time.sleep(0.01)
    
    # Mark items with even IDs as completed
    for item_id in item_ids:
        if item_id % 2 == 0:
            r = client.put(f"/action-items/{item_id}/complete")
            assert r.status_code == 200, f"Failed to complete item {item_id}: {r.text}"
    
    # Test completed=True with limit=3
    r = client.get("/action-items/", params={"completed": True, "limit": 3})
    assert r.status_code == 200, f"Failed to get completed items: {r.text}"
    items = r.json()
    assert len(items) <= 3, f"Expected at most 3 items, got {len(items)}"
    
    # Verify all returned items are completed
    for item in items:
        assert item["completed"] is True, f"Item {item['id']} should be completed but is not"
    
    # Verify at most 3 items returned
    assert len(items) <= 3, f"Expected at most 3 items, got {len(items)}"


def test_sorting_fallback_invalid_field(client):
    # Create 2 items
    for i in range(2):
        payload = {"description": f"Task {i}"}
        r = client.post("/action-items/", json=payload)
        assert r.status_code == 201, f"Failed to create item {i}: {r.text}"
        time.sleep(0.01)
    
    # Test sort="nonexistent_field"
    r = client.get("/action-items/", params={"sort": "nonexistent_field"})
    # Should return 200 (not crash)
    assert r.status_code == 200, f"Expected 200 status code with invalid sort field, got {r.status_code}: {r.text}"
    # Should return items (fallback behavior)
    items = r.json()
    assert isinstance(items, list), f"Expected list, got {type(items)}"
    assert len(items) >= 2, f"Expected at least 2 items, got {len(items)}"
