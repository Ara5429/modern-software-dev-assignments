def test_create_mood(client):
    """Test creating a mood entry"""
    response = client.post(
        "/api/moods",
        json={"date": "2024-01-15T10:00:00", "mood": "happy"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["mood"] == "happy"
    assert "id" in data


def test_get_all_moods(client):
    """Test listing all moods"""
    # Create a mood first
    client.post("/api/moods", json={"mood": "happy"})
    
    response = client.get("/api/moods")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_create_note_with_mood(client):
    """Test creating a note linked to a mood"""
    # First create a mood
    mood_response = client.post(
        "/api/moods",
        json={"mood": "sad"}
    )
    assert mood_response.status_code == 200
    mood_id = mood_response.json()["id"]
    
    # Create note with mood
    note_response = client.post(
        "/api/notes",
        json={
            "title": "Sad Day",
            "content": "Not feeling great",
            "mood_id": mood_id
        }
    )
    assert note_response.status_code == 200
    note_data = note_response.json()
    assert note_data["mood_id"] == mood_id
    
    # Verify relationship
    if "mood_entry" in note_data and note_data["mood_entry"]:
        assert note_data["mood_entry"]["id"] == mood_id
        assert note_data["mood_entry"]["mood"] == "sad"


def test_unique_mood_per_day(client):
    """Test that only one mood per day is allowed"""
    # Create first mood
    date_str = "2024-01-20T10:00:00"
    response1 = client.post(
        "/api/moods",
        json={"date": date_str, "mood": "happy"}
    )
    assert response1.status_code == 200
    
    # Try to create another mood on same day - should fail with unique constraint
    response2 = client.post(
        "/api/moods",
        json={"date": date_str, "mood": "sad"}
    )
    # Should fail due to unique constraint on date
    assert response2.status_code == 409  # Conflict - mood already exists for this date
