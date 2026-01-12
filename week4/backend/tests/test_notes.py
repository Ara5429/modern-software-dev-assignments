def test_create_and_list_notes(client):
    payload = {"title": "Test", "content": "Hello world"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["title"] == "Test"

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1

    r = client.get("/notes/search/")
    assert r.status_code == 200

    r = client.get("/notes/search/", params={"q": "Hello"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) >= 1


def test_create_note_returns_id(client):
    payload = {"title": "New Note", "content": "Some content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 201
    data = r.json()
    assert "id" in data
    assert isinstance(data["id"], int)
    assert data["title"] == "New Note"
    assert data["content"] == "Some content"


def test_create_note_missing_title(client):
    payload = {"content": "Only content"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422


def test_create_note_missing_content(client):
    payload = {"title": "Only title"}
    r = client.post("/notes/", json=payload)
    assert r.status_code == 422


def test_create_note_empty_payload(client):
    r = client.post("/notes/", json={})
    assert r.status_code == 422


def test_list_notes_empty(client):
    r = client.get("/notes/")
    assert r.status_code == 200
    assert r.json() == []


def test_list_notes_multiple(client):
    for i in range(3):
        client.post("/notes/", json={"title": f"Note {i}", "content": f"Content {i}"})

    r = client.get("/notes/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 3


def test_get_note_by_id(client):
    payload = {"title": "Specific Note", "content": "Specific Content"}
    create_response = client.post("/notes/", json=payload)
    note_id = create_response.json()["id"]

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == note_id
    assert data["title"] == "Specific Note"
    assert data["content"] == "Specific Content"


def test_get_note_not_found(client):
    r = client.get("/notes/99999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Note not found"


def test_get_note_invalid_id(client):
    r = client.get("/notes/invalid")
    assert r.status_code == 422


def test_search_notes_no_query_returns_all(client):
    client.post("/notes/", json={"title": "First", "content": "AAA"})
    client.post("/notes/", json={"title": "Second", "content": "BBB"})

    r = client.get("/notes/search/")
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2


def test_search_notes_by_title(client):
    client.post("/notes/", json={"title": "Python Guide", "content": "Learn Python"})
    client.post("/notes/", json={"title": "Java Guide", "content": "Learn Java"})

    r = client.get("/notes/search/", params={"q": "Python"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1
    assert items[0]["title"] == "Python Guide"


def test_search_notes_by_content(client):
    client.post("/notes/", json={"title": "Note A", "content": "Contains special keyword"})
    client.post("/notes/", json={"title": "Note B", "content": "Regular content"})

    r = client.get("/notes/search/", params={"q": "special"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 1
    assert items[0]["title"] == "Note A"


def test_search_notes_matches_title_and_content(client):
    client.post("/notes/", json={"title": "Meeting notes", "content": "Discussed project"})
    client.post("/notes/", json={"title": "Shopping list", "content": "Meeting supplies"})

    r = client.get("/notes/search/", params={"q": "Meeting"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2


def test_search_notes_no_match(client):
    client.post("/notes/", json={"title": "Hello", "content": "World"})

    r = client.get("/notes/search/", params={"q": "xyz123notfound"})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 0


def test_search_notes_empty_query_returns_all(client):
    client.post("/notes/", json={"title": "Note 1", "content": "Content 1"})
    client.post("/notes/", json={"title": "Note 2", "content": "Content 2"})

    r = client.get("/notes/search/", params={"q": ""})
    assert r.status_code == 200
    items = r.json()
    assert len(items) == 2


def test_delete_note(client):
    create_response = client.post("/notes/", json={"title": "To Delete", "content": "Will be deleted"})
    note_id = create_response.json()["id"]

    r = client.delete(f"/notes/{note_id}")
    assert r.status_code == 204

    r = client.get(f"/notes/{note_id}")
    assert r.status_code == 404


def test_delete_note_not_found(client):
    r = client.delete("/notes/99999")
    assert r.status_code == 404
    assert r.json()["detail"] == "Note not found"


def test_delete_note_invalid_id(client):
    r = client.delete("/notes/invalid")
    assert r.status_code == 422


def test_delete_note_removes_from_list(client):
    client.post("/notes/", json={"title": "Note A", "content": "Content A"})
    create_response = client.post("/notes/", json={"title": "Note B", "content": "Content B"})
    note_b_id = create_response.json()["id"]
    client.post("/notes/", json={"title": "Note C", "content": "Content C"})

    r = client.get("/notes/")
    assert len(r.json()) == 3

    client.delete(f"/notes/{note_b_id}")

    r = client.get("/notes/")
    items = r.json()
    assert len(items) == 2
    titles = [item["title"] for item in items]
    assert "Note B" not in titles
