def test_create_tag(client):
    """Test creating a tag"""
    response = client.post(
        "/api/tags",
        json={"name": "Important", "color": "#FF0000"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Important"
    assert data["color"] == "#FF0000"


def test_get_all_tags(client):
    """Test listing all tags"""
    response = client.get("/api/tags")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_tag_to_note(client):
    """Test adding tags to a note"""
    # Create a tag
    tag_response = client.post(
        "/api/tags",
        json={"name": "Important", "color": "#FF0000"}
    )
    assert tag_response.status_code == 200
    tag_id = tag_response.json()["id"]
    
    # Create a note with the tag
    note_response = client.post(
        "/api/notes",
        json={
            "title": "Tagged Note",
            "content": "This has tags",
            "tag_ids": [tag_id]
        }
    )
    assert note_response.status_code == 200
    note_data = note_response.json()
    assert len(note_data["tags"]) == 1
    assert note_data["tags"][0]["id"] == tag_id
