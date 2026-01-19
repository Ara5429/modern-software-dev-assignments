# Version 1: FastAPI + Vue.js Mood Tracker

A full-stack mood tracking and note-taking application built with FastAPI and Vue 3.

## 📋 Features

- 📝 **Notes Management**: Create, read, update, and delete notes
- 😊 **Mood Tracking**: Track daily moods (happy, neutral, sad, angry, tired)
- 🏷️ **Tags System**: Organize notes with tags
- ✅ **Action Items**: Manage tasks and to-dos
- 🔗 **Relationships**: Link notes with moods and tags
- 📊 **Statistics**: View mood trends (coming soon in frontend)

## 🛠️ Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Lightweight database
- **Pydantic**: Data validation
- **Pytest**: Testing framework

### Frontend
- **Vue 3**: Progressive JavaScript framework
- **Vite**: Fast build tool
- **Chart.js**: Data visualization
- **Tailwind CSS**: Utility-first CSS
- **Axios**: HTTP client

## 📁 Project Structure
```
version1-fastapi-vue/
├── backend/
│   ├── app/
│   │   ├── routers/          # API endpoints
│   │   │   ├── notes.py
│   │   │   ├── moods.py
│   │   │   ├── tags.py
│   │   │   └── action_items.py
│   │   ├── models.py         # Database models
│   │   ├── schemas.py        # Pydantic schemas
│   │   ├── database.py       # DB connection
│   │   └── main.py           # FastAPI app
│   ├── tests/                # Pytest tests
│   ├── requirements.txt      # Python dependencies
│   ├── reset_db.py          # Database reset script
│   └── app.db               # SQLite database (auto-created)
├── frontend/
│   ├── src/
│   │   ├── components/      # Vue components
│   │   ├── views/           # Vue pages
│   │   ├── App.vue          # Root component
│   │   └── main.js          # Entry point
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 🚀 Getting Started

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database**:
   ```bash
   python reset_db.py
   # Type 'yes' when prompted
   ```

5. **Run the server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run development server**:
   ```bash
   npm run dev
   ```

The frontend will be available at `http://localhost:5173`

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
pytest tests/ -v
```

### Test Coverage

All endpoints are tested:
- ✅ Notes CRUD operations
- ✅ Moods CRUD operations
- ✅ Tags CRUD operations
- ✅ Action Items CRUD operations
- ✅ Relationships (notes with moods and tags)

## 📚 API Documentation

Once the backend server is running, visit:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🔧 Database Models

### Note
- `id`: Primary key
- `title`: Note title (max 200 chars)
- `content`: Note content (text)
- `mood_id`: Foreign key to MoodEntry (optional)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### MoodEntry
- `id`: Primary key
- `date`: Date of mood entry (unique, one per day)
- `mood`: Mood type (happy, neutral, sad, angry, tired)
- `created_at`: Creation timestamp

### Tag
- `id`: Primary key
- `name`: Tag name (unique, max 50 chars)
- `color`: Hex color code (default: #3B82F6)
- `created_at`: Creation timestamp

### ActionItem
- `id`: Primary key
- `description`: Task description (max 500 chars)
- `completed`: Completion status (boolean)
- `created_at`: Creation timestamp

## 🔗 Relationships

- **Note ↔ MoodEntry**: One-to-one (Note.mood_id → MoodEntry.id)
- **Note ↔ Tag**: Many-to-many (via note_tags association table)
- **Cascade deletes**: Tags are removed from notes when deleted

## 🛡️ Security

- **Semgrep**: Security scanning configured in `.semgrep.yml`
- **Input validation**: Pydantic schemas validate all inputs
- **CORS**: Configured for frontend origins

## 📝 API Endpoints

### Notes
- `GET /api/notes` - List all notes
- `GET /api/notes/{id}` - Get a note
- `POST /api/notes` - Create a note
- `PUT /api/notes/{id}` - Update a note
- `DELETE /api/notes/{id}` - Delete a note

### Moods
- `GET /api/moods` - List all moods
- `GET /api/moods/{id}` - Get a mood
- `GET /api/moods/weekly` - Get weekly moods
- `GET /api/moods/stats/weekly` - Get mood statistics
- `POST /api/moods` - Create a mood
- `PUT /api/moods/{id}` - Update a mood
- `DELETE /api/moods/{id}` - Delete a mood

### Tags
- `GET /api/tags` - List all tags
- `GET /api/tags/{id}` - Get a tag
- `POST /api/tags` - Create a tag
- `PUT /api/tags/{id}` - Update a tag
- `DELETE /api/tags/{id}` - Delete a tag

### Action Items
- `GET /api/action-items` - List all action items
- `GET /api/action-items/{id}` - Get an action item
- `POST /api/action-items` - Create an action item
- `PUT /api/action-items/{id}` - Update an action item
- `DELETE /api/action-items/{id}` - Delete an action item

## 🐛 Troubleshooting

### Database Issues
If you encounter database errors:
```bash
cd backend
python reset_db.py
```

### Port Already in Use
Change the port:
```bash
uvicorn app.main:app --reload --port 8001
```

### Test Failures
Make sure the database is clean:
```bash
cd backend
pytest tests/ -v --tb=short
```

## 📄 License

MIT
