def test_create_note_simple(client):
    """Test creating a basic note without mood"""
    response = client.post(
        "/api/notes",
        json={"title": "Test", "content": "Content"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test"
    assert data["content"] == "Content"
    assert "id" in data


def test_get_all_notes(client):
    """Test listing all notes"""
    response = client.get("/api/notes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_single_note(client):
    """Test getting a specific note"""
    # First create a note
    create_response = client.post(
        "/api/notes",
        json={"title": "Single", "content": "Test"}
    )
    note_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(f"/api/notes/{note_id}")
    assert response.status_code == 200
    assert response.json()["id"] == note_id


def test_update_note(client):
    """Test updating a note"""
    # Create
    create_response = client.post(
        "/api/notes",
        json={"title": "Original", "content": "Original content"}
    )
    note_id = create_response.json()["id"]
    
    # Update
    update_response = client.put(
        f"/api/notes/{note_id}",
        json={"title": "Updated", "content": "Updated content"}
    )
    assert update_response.status_code == 200
    assert update_response.json()["title"] == "Updated"


def test_delete_note(client):
    """Test deleting a note"""
    # Create
    create_response = client.post(
        "/api/notes",
        json={"title": "Delete Me", "content": "Bye"}
    )
    note_id = create_response.json()["id"]
    
    # Delete
    delete_response = client.delete(f"/api/notes/{note_id}")
    assert delete_response.status_code == 200
    
    # Verify deleted
    get_response = client.get(f"/api/notes/{note_id}")
    assert get_response.status_code == 404
