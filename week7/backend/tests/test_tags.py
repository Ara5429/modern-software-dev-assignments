def test_create_tag_success(client):
    """Test successful tag creation"""
    payload = {"name": "Important", "color": "#FF0000"}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 201, r.text
    tag = r.json()
    assert tag["name"] == "Important"
    assert tag["color"] == "#FF0000"
    assert "id" in tag
    assert "created_at" in tag
    assert "updated_at" in tag


def test_create_tag_validation_name_empty(client):
    """Test tag creation with empty name is rejected"""
    payload = {"name": "", "color": "#FF0000"}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 422

    # Test whitespace-only name is rejected
    payload = {"name": "   ", "color": "#FF0000"}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 422


def test_create_tag_validation_name_too_long(client):
    """Test tag creation with name exceeding 50 characters is rejected"""
    payload = {"name": "a" * 51, "color": "#FF0000"}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 422


def test_create_tag_validation_invalid_color(client):
    """Test tag creation with invalid color format is rejected"""
    # Missing #
    payload = {"name": "Test", "color": "FF0000"}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 422

    # Invalid hex
    payload = {"name": "Test", "color": "#GGGGGG"}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 422

    # Wrong length
    payload = {"name": "Test", "color": "#FF00"}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 422

    # Valid color should work
    payload = {"name": "Test", "color": "#FF0000"}
    r = client.post("/tags/", json=payload)
    assert r.status_code == 201


def test_list_tags(client):
    """Test listing all tags"""
    # Create multiple tags
    tag1 = client.post("/tags/", json={"name": "Urgent", "color": "#FF0000"}).json()
    tag2 = client.post("/tags/", json={"name": "Review", "color": "#00FF00"}).json()
    tag3 = client.post("/tags/", json={"name": "Done", "color": "#0000FF"}).json()

    # List all tags
    r = client.get("/tags/")
    assert r.status_code == 200
    tags = r.json()
    assert len(tags) >= 3

    # Verify created tags are in the list
    tag_ids = [tag["id"] for tag in tags]
    assert tag1["id"] in tag_ids
    assert tag2["id"] in tag_ids
    assert tag3["id"] in tag_ids


def test_add_tag_to_note_success(client):
    """Test adding a tag to a note"""
    # Create a note
    note_payload = {"title": "Test Note", "content": "Test content"}
    note_r = client.post("/notes/", json=note_payload)
    assert note_r.status_code == 201
    note = note_r.json()
    note_id = note["id"]

    # Create a tag
    tag_payload = {"name": "Important", "color": "#FF0000"}
    tag_r = client.post("/tags/", json=tag_payload)
    assert tag_r.status_code == 201
    tag = tag_r.json()
    tag_id = tag["id"]

    # Add tag to note
    r = client.post(f"/notes/{note_id}/tags/{tag_id}")
    assert r.status_code == 204

    # Verify tag is associated with note
    note_r = client.get(f"/notes/{note_id}")
    assert note_r.status_code == 200
    note_with_tags = note_r.json()
    assert "tags" in note_with_tags
    assert len(note_with_tags["tags"]) == 1
    assert note_with_tags["tags"][0]["id"] == tag_id
    assert note_with_tags["tags"][0]["name"] == "Important"


def test_remove_tag_from_note_success(client):
    """Test removing a tag from a note"""
    # Create a note
    note_payload = {"title": "Test Note", "content": "Test content"}
    note_r = client.post("/notes/", json=note_payload)
    assert note_r.status_code == 201
    note = note_r.json()
    note_id = note["id"]

    # Create a tag
    tag_payload = {"name": "Important", "color": "#FF0000"}
    tag_r = client.post("/tags/", json=tag_payload)
    assert tag_r.status_code == 201
    tag = tag_r.json()
    tag_id = tag["id"]

    # Add tag to note
    r = client.post(f"/notes/{note_id}/tags/{tag_id}")
    assert r.status_code == 204

    # Verify tag is added
    note_r = client.get(f"/notes/{note_id}")
    assert len(note_r.json()["tags"]) == 1

    # Remove tag from note
    r = client.delete(f"/notes/{note_id}/tags/{tag_id}")
    assert r.status_code == 204

    # Verify tag is removed
    note_r = client.get(f"/notes/{note_id}")
    assert note_r.status_code == 200
    note_with_tags = note_r.json()
    assert "tags" in note_with_tags
    assert len(note_with_tags["tags"]) == 0


def test_note_with_multiple_tags(client):
    """Test that a note can have multiple tags"""
    # Create a note
    note_payload = {"title": "Test Note", "content": "Test content"}
    note_r = client.post("/notes/", json=note_payload)
    assert note_r.status_code == 201
    note = note_r.json()
    note_id = note["id"]

    # Create multiple tags
    tag1 = client.post("/tags/", json={"name": "Urgent", "color": "#FF0000"}).json()
    tag2 = client.post("/tags/", json={"name": "Review", "color": "#00FF00"}).json()
    tag3 = client.post("/tags/", json={"name": "Done", "color": "#0000FF"}).json()

    # Add all tags to note
    client.post(f"/notes/{note_id}/tags/{tag1['id']}")
    client.post(f"/notes/{note_id}/tags/{tag2['id']}")
    client.post(f"/notes/{note_id}/tags/{tag3['id']}")

    # Verify note has all tags
    note_r = client.get(f"/notes/{note_id}")
    assert note_r.status_code == 200
    note_with_tags = note_r.json()
    assert len(note_with_tags["tags"]) == 3

    tag_ids = [tag["id"] for tag in note_with_tags["tags"]]
    assert tag1["id"] in tag_ids
    assert tag2["id"] in tag_ids
    assert tag3["id"] in tag_ids


def test_tag_with_multiple_notes(client):
    """Test that a tag can belong to multiple notes"""
    # Create multiple notes
    note1 = client.post("/notes/", json={"title": "Note 1", "content": "Content 1"}).json()
    note2 = client.post("/notes/", json={"title": "Note 2", "content": "Content 2"}).json()
    note3 = client.post("/notes/", json={"title": "Note 3", "content": "Content 3"}).json()

    # Create a tag
    tag = client.post("/tags/", json={"name": "Shared", "color": "#FF0000"}).json()
    tag_id = tag["id"]

    # Add tag to all notes
    client.post(f"/notes/{note1['id']}/tags/{tag_id}")
    client.post(f"/notes/{note2['id']}/tags/{tag_id}")
    client.post(f"/notes/{note3['id']}/tags/{tag_id}")

    # Verify tag is associated with all notes
    note1_r = client.get(f"/notes/{note1['id']}")
    assert len(note1_r.json()["tags"]) == 1
    assert note1_r.json()["tags"][0]["id"] == tag_id

    note2_r = client.get(f"/notes/{note2['id']}")
    assert len(note2_r.json()["tags"]) == 1
    assert note2_r.json()["tags"][0]["id"] == tag_id

    note3_r = client.get(f"/notes/{note3['id']}")
    assert len(note3_r.json()["tags"]) == 1
    assert note3_r.json()["tags"][0]["id"] == tag_id


def test_list_notes_includes_tags(client):
    """Test that listing notes includes tags"""
    # Create notes
    note1 = client.post("/notes/", json={"title": "Note 1", "content": "Content 1"}).json()
    note2 = client.post("/notes/", json={"title": "Note 2", "content": "Content 2"}).json()

    # Create tags
    tag1 = client.post("/tags/", json={"name": "Urgent", "color": "#FF0000"}).json()
    tag2 = client.post("/tags/", json={"name": "Review", "color": "#00FF00"}).json()

    # Add tags to notes
    client.post(f"/notes/{note1['id']}/tags/{tag1['id']}")
    client.post(f"/notes/{note2['id']}/tags/{tag2['id']}")

    # List notes
    r = client.get("/notes/")
    assert r.status_code == 200
    notes = r.json()

    # Find our notes in the list
    note1_found = next(n for n in notes if n["id"] == note1["id"])
    note2_found = next(n for n in notes if n["id"] == note2["id"])

    # Verify tags are included
    assert "tags" in note1_found
    assert len(note1_found["tags"]) == 1
    assert note1_found["tags"][0]["id"] == tag1["id"]

    assert "tags" in note2_found
    assert len(note2_found["tags"]) == 1
    assert note2_found["tags"][0]["id"] == tag2["id"]


def test_delete_tag_success(client):
    """Test successful tag deletion"""
    # Create a tag
    tag_payload = {"name": "To Delete", "color": "#FF0000"}
    tag_r = client.post("/tags/", json=tag_payload)
    assert tag_r.status_code == 201
    tag = tag_r.json()
    tag_id = tag["id"]

    # Verify tag exists
    tags_r = client.get("/tags/")
    tag_ids = [t["id"] for t in tags_r.json()]
    assert tag_id in tag_ids

    # Delete tag
    r = client.delete(f"/tags/{tag_id}")
    assert r.status_code == 204

    # Verify tag is deleted
    tags_r = client.get("/tags/")
    tag_ids = [t["id"] for t in tags_r.json()]
    assert tag_id not in tag_ids


def test_add_tag_to_nonexistent_note(client):
    """Test adding tag to non-existent note returns 404"""
    # Create a tag
    tag_payload = {"name": "Test", "color": "#FF0000"}
    tag_r = client.post("/tags/", json=tag_payload)
    assert tag_r.status_code == 201
    tag = tag_r.json()
    tag_id = tag["id"]

    # Try to add tag to non-existent note
    r = client.post(f"/notes/99999/tags/{tag_id}")
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()
