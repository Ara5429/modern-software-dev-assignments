import time

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


def test_pagination_notes_basic(client):
    # Create 15 notes with time delays
    for i in range(15):
        payload = {"title": f"Note {i}", "content": f"Content {i}"}
        r = client.post("/notes/", json=payload)
        assert r.status_code == 201, f"Failed to create note {i}: {r.text}"
        time.sleep(0.01)
    
    # Test skip=0, limit=10 returns 10 notes
    r = client.get("/notes/", params={"skip": 0, "limit": 10})
    assert r.status_code == 200, f"Failed to get first page: {r.text}"
    first_page = r.json()
    assert len(first_page) == 10, f"Expected 10 notes, got {len(first_page)}"
    
    # Test skip=10, limit=10 returns 5 notes (remaining)
    r = client.get("/notes/", params={"skip": 10, "limit": 10})
    assert r.status_code == 200, f"Failed to get second page: {r.text}"
    second_page = r.json()
    assert len(second_page) == 5, f"Expected 5 notes, got {len(second_page)}"


def test_pagination_edge_cases_notes(client):
    # Create 5 notes
    for i in range(5):
        payload = {"title": f"Note {i}", "content": f"Content {i}"}
        r = client.post("/notes/", json=payload)
        assert r.status_code == 201, f"Failed to create note {i}: {r.text}"
        time.sleep(0.01)
    
    # Test skip=100 returns empty list
    r = client.get("/notes/", params={"skip": 100})
    assert r.status_code == 200, f"Failed to get notes with skip=100: {r.text}"
    notes = r.json()
    assert len(notes) == 0, f"Expected empty list, got {len(notes)} notes"
    
    # Test limit=1 returns exactly 1 note
    r = client.get("/notes/", params={"limit": 1})
    assert r.status_code == 200, f"Failed to get notes with limit=1: {r.text}"
    notes = r.json()
    assert len(notes) == 1, f"Expected 1 note, got {len(notes)}"


def test_sorting_notes_by_title(client):
    # Create notes with titles: "CCC", "AAA", "BBB" (with delays)
    titles = ["CCC", "AAA", "BBB"]
    note_ids = []
    for title in titles:
        payload = {"title": title, "content": f"Content for {title}"}
        r = client.post("/notes/", json=payload)
        assert r.status_code == 201, f"Failed to create note with title {title}: {r.text}"
        note_ids.append(r.json()["id"])
        time.sleep(0.01)
    
    # Test sort="title" returns AAA, BBB, CCC order
    r = client.get("/notes/", params={"sort": "title", "limit": 10})
    assert r.status_code == 200, f"Failed to get notes sorted by title: {r.text}"
    notes_asc = r.json()
    # Find our notes in the list (there might be other notes)
    our_notes = [note for note in notes_asc if note["id"] in note_ids]
    assert len(our_notes) == 3, f"Expected 3 notes, got {len(our_notes)}"
    assert our_notes[0]["title"] == "AAA", f"Expected AAA first, got {our_notes[0]['title']}"
    assert our_notes[1]["title"] == "BBB", f"Expected BBB second, got {our_notes[1]['title']}"
    assert our_notes[2]["title"] == "CCC", f"Expected CCC third, got {our_notes[2]['title']}"
    
    # Test sort="-title" returns CCC, BBB, AAA order
    r = client.get("/notes/", params={"sort": "-title", "limit": 10})
    assert r.status_code == 200, f"Failed to get notes sorted by -title: {r.text}"
    notes_desc = r.json()
    # Find our notes in the list
    our_notes_desc = [note for note in notes_desc if note["id"] in note_ids]
    assert len(our_notes_desc) == 3, f"Expected 3 notes, got {len(our_notes_desc)}"
    assert our_notes_desc[0]["title"] == "CCC", f"Expected CCC first, got {our_notes_desc[0]['title']}"
    assert our_notes_desc[1]["title"] == "BBB", f"Expected BBB second, got {our_notes_desc[1]['title']}"
    assert our_notes_desc[2]["title"] == "AAA", f"Expected AAA third, got {our_notes_desc[2]['title']}"


def test_sorting_notes_by_created_at(client):
    # Create 3 notes with delays, store IDs
    note_ids = []
    for i in range(3):
        payload = {"title": f"Note {i}", "content": f"Content {i}"}
        r = client.post("/notes/", json=payload)
        assert r.status_code == 201, f"Failed to create note {i}: {r.text}"
        note_ids.append(r.json()["id"])
        time.sleep(0.01)
    
    # Test sort="-created_at" returns newest first
    r = client.get("/notes/", params={"sort": "-created_at", "limit": 10})
    assert r.status_code == 200, f"Failed to get notes sorted by -created_at: {r.text}"
    notes_desc = r.json()
    assert len(notes_desc) >= 3, f"Expected at least 3 notes, got {len(notes_desc)}"
    # The last created note (last in note_ids) should be first in the sorted list
    assert notes_desc[0]["id"] == note_ids[-1], f"Expected newest note {note_ids[-1]} first, got {notes_desc[0]['id']}"
    
    # Test sort="created_at" returns oldest first
    r = client.get("/notes/", params={"sort": "created_at", "limit": 10})
    assert r.status_code == 200, f"Failed to get notes sorted by created_at: {r.text}"
    notes_asc = r.json()
    assert len(notes_asc) >= 3, f"Expected at least 3 notes, got {len(notes_asc)}"
    # The first created note (first in note_ids) should be first in the sorted list
    # Note: We need to find our notes in the list since there might be other notes
    found_ids = [note["id"] for note in notes_asc if note["id"] in note_ids]
    assert found_ids[0] == note_ids[0], f"Expected oldest note {note_ids[0]} first, got {found_ids[0] if found_ids else 'none'}"


def test_search_with_pagination(client):
    # Create 10 notes: 5 with "project" in title, 5 with "meeting"
    for i in range(5):
        payload = {"title": f"project note {i}", "content": f"Content {i}"}
        r = client.post("/notes/", json=payload)
        assert r.status_code == 201, f"Failed to create project note {i}: {r.text}"
        time.sleep(0.01)
    
    for i in range(5):
        payload = {"title": f"meeting note {i}", "content": f"Content {i}"}
        r = client.post("/notes/", json=payload)
        assert r.status_code == 201, f"Failed to create meeting note {i}: {r.text}"
        time.sleep(0.01)
    
    # Test q="project" with limit=3
    r = client.get("/notes/", params={"q": "project", "limit": 3})
    assert r.status_code == 200, f"Failed to search for 'project': {r.text}"
    notes = r.json()
    
    # Verify all returned notes contain "project"
    for note in notes:
        assert "project" in note["title"].lower(), f"Note {note['id']} title '{note['title']}' should contain 'project'"
    
    # Verify at most 3 notes returned
    assert len(notes) <= 3, f"Expected at most 3 notes, got {len(notes)}"


def test_search_and_sorting_combined(client):
    # Create notes with titles: "Test BBB", "Test AAA", "Other CCC"
    titles = ["Test BBB", "Test AAA", "Other CCC"]
    note_ids = []
    for title in titles:
        payload = {"title": title, "content": f"Content for {title}"}
        r = client.post("/notes/", json=payload)
        assert r.status_code == 201, f"Failed to create note with title {title}: {r.text}"
        note_ids.append(r.json()["id"])
        time.sleep(0.01)
    
    # Test q="Test", sort="title"
    r = client.get("/notes/", params={"q": "Test", "sort": "title"})
    assert r.status_code == 200, f"Failed to search and sort: {r.text}"
    notes = r.json()
    
    # Verify results contain "Test" and are sorted
    assert len(notes) >= 2, f"Expected at least 2 notes with 'Test', got {len(notes)}"
    for note in notes:
        assert "test" in note["title"].lower(), f"Note {note['id']} title '{note['title']}' should contain 'Test'"
    
    # Find our "Test" notes in the results
    test_notes = [note for note in notes if note["id"] in note_ids]
    assert len(test_notes) == 2, f"Expected 2 'Test' notes, got {len(test_notes)}"
    # Verify they are sorted: "Test AAA" should come before "Test BBB"
    test_titles = [note["title"] for note in test_notes]
    assert "Test AAA" in test_titles[0], f"Expected 'Test AAA' first, got '{test_titles[0]}'"
    assert "Test BBB" in test_titles[1], f"Expected 'Test BBB' second, got '{test_titles[1]}'"


def test_all_features_combined(client):
    # Create diverse notes with various titles
    titles = ["task alpha", "task beta", "task gamma", "other note", "another task"]
    for title in titles:
        payload = {"title": title, "content": f"Content for {title}"}
        r = client.post("/notes/", json=payload)
        assert r.status_code == 201, f"Failed to create note with title {title}: {r.text}"
        time.sleep(0.01)
    
    # Test q="task", skip=1, limit=2, sort="title"
    r = client.get("/notes/", params={"q": "task", "skip": 1, "limit": 2, "sort": "title"})
    assert r.status_code == 200, f"Failed to combine search, pagination, and sorting: {r.text}"
    notes = r.json()
    
    # Verify search, pagination, and sorting all work together
    assert len(notes) <= 2, f"Expected at most 2 notes (limit=2), got {len(notes)}"
    
    # Verify all returned notes contain "task"
    for note in notes:
        assert "task" in note["title"].lower(), f"Note {note['id']} title '{note['title']}' should contain 'task'"
    
    # Verify they are sorted by title (alphabetically)
    if len(notes) >= 2:
        assert notes[0]["title"] < notes[1]["title"], f"Notes should be sorted: '{notes[0]['title']}' should come before '{notes[1]['title']}'"
