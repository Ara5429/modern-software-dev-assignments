def test_create_list_and_patch_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"
    assert "created_at" in data and "updated_at" in data

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/", params={"q": "Hello", "limit": 10, "sort": "-created_at"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    note_id = data["id"]
    r = client.patch(f"/notes/{note_id}", json={"title": "Updated"})
    assert r.status_code == 200
    patched = r.json()
    assert patched["title"] == "Updated"


def test_delete_note_success(client):
    # Create a note first
    payload = {"title": "Note to delete", "content": "This will be deleted"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    note = r.json()
    note_id = note["id"]

    # Verify it exists in the list
    r = client.get("/notes/")
    assert r.status_code == 200
    notes = r.json()
    assert any(n["id"] == note_id for n in notes)

    # Delete it
    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204
    assert r.content == b""

    # Verify it's actually removed from database by checking list
    r = client.get("/notes/")
    assert r.status_code == 200
    notes = r.json()
    assert not any(n["id"] == note_id for n in notes)

    # Also verify trying to delete again returns 404
    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 404


def test_delete_note_not_found(client):
    # Try to delete a non-existent note
    r = client.delete("/notes/99999")
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()


def test_create_note_validation_title_empty(client):
    # Test empty title is rejected
    payload = {"title": "", "content": "Some content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422

    # Test whitespace-only title is rejected
    payload = {"title": "   ", "content": "Some content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422


def test_create_note_validation_title_too_long(client):
    # Test title exceeding 200 characters is rejected
    payload = {"title": "a" * 201, "content": "Some content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422


def test_create_note_validation_content_empty(client):
    # Test empty content is rejected
    payload = {"title": "Valid title", "content": ""}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422

    # Test whitespace-only content is rejected
    payload = {"title": "Valid title", "content": "   "}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422


def test_create_note_validation_success(client):
    # Test valid title (1-200 chars) and non-empty content are accepted
    payload = {"title": "Valid Title", "content": "Valid content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    note = r.json()
    assert note["title"] == "Valid Title"
    assert note["content"] == "Valid content"

    # Test minimum length title (1 character)
    payload = {"title": "A", "content": "Content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text

    # Test maximum length title (200 characters)
    payload = {"title": "a" * 200, "content": "Content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
