def test_create_action_item(client):
    """Test creating an action item"""
    response = client.post(
        "/api/action-items",
        json={"description": "Do something"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Do something"
    assert data["completed"] is False


def test_complete_action_item(client):
    """Test marking action item as complete"""
    # Create
    create_response = client.post(
        "/api/action-items",
        json={"description": "Complete this"}
    )
    item_id = create_response.json()["id"]
    
    # Mark complete
    update_response = client.put(
        f"/api/action-items/{item_id}",
        json={"completed": True}
    )
    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True
