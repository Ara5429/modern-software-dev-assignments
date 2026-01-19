# Mood Tracking Notes API - Backend

FastAPI backend for the mood tracking notes application.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once the server is running, you can access:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Notes
- `GET /api/notes/` - Get all notes
- `GET /api/notes/{note_id}` - Get a specific note
- `POST /api/notes/` - Create a new note
- `PUT /api/notes/{note_id}` - Update a note
- `DELETE /api/notes/{note_id}` - Delete a note

### Action Items
- `GET /api/action-items/` - Get all action items
- `GET /api/action-items/{item_id}` - Get a specific action item
- `POST /api/action-items/` - Create a new action item
- `PUT /api/action-items/{item_id}` - Update an action item
- `DELETE /api/action-items/{item_id}` - Delete an action item

### Tags
- `GET /api/tags/` - Get all tags
- `GET /api/tags/{tag_id}` - Get a specific tag
- `POST /api/tags/` - Create a new tag
- `PUT /api/tags/{tag_id}` - Update a tag
- `DELETE /api/tags/{tag_id}` - Delete a tag

### Moods
- `GET /api/moods/` - Get all mood entries
- `GET /api/moods/weekly` - Get weekly mood entries (last 7 days)
- `GET /api/moods/stats/weekly` - Get weekly mood statistics
- `GET /api/moods/{mood_id}` - Get a specific mood entry
- `POST /api/moods/` - Create a new mood entry
- `PUT /api/moods/{mood_id}` - Update a mood entry
- `DELETE /api/moods/{mood_id}` - Delete a mood entry

## Database

The application uses SQLite database (`mood_tracker.db`) which is automatically created when you first run the application.

## Models

- **Note**: id, title, content, mood_id, created_at, updated_at
- **ActionItem**: id, description, completed, created_at
- **Tag**: id, name, color
- **MoodEntry**: id, date, mood, note_id, created_at
- **note_tags**: Association table for Note-Tag many-to-many relationship
