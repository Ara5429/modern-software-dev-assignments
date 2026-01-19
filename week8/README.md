# Mood Tracking Notes Application

A full-stack application for tracking moods and managing notes, built with FastAPI and Vue 3.

## Features

- **Notes Management**: Create, edit, and delete notes with rich content
- **Action Items**: Track action items linked to notes
- **Mood Tracking**: Track daily moods (happy, neutral, sad, angry, tired)
- **Tags**: Organize notes with colored tags
- **Statistics**: View weekly and monthly mood statistics
- **Dark Mode**: Toggle between light and dark themes
- **Responsive Design**: Works on desktop and mobile devices

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routers/
│       ├── __init__.py
│       ├── notes.py
│       ├── action_items.py
│       ├── tags.py
│       └── moods.py
├── requirements.txt
├── .env.example
└── README.md

frontend/
├── src/
│   ├── components/
│   │   ├── NotesList.vue
│   │   ├── NoteForm.vue
│   │   ├── ActionItemsList.vue
│   │   ├── MoodTracker.vue
│   │   ├── MoodChart.vue
│   │   └── TagsManager.vue
│   ├── views/
│   │   ├── Home.vue
│   │   ├── Notes.vue
│   │   └── Moods.vue
│   ├── App.vue
│   ├── main.js
│   ├── router.js
│   ├── api.js
│   └── style.css
├── index.html
├── package.json
├── vite.config.js
├── tailwind.config.js
└── postcss.config.js
```

## Setup Instructions

### Backend Setup

1. **Navigate to the backend directory**:
   ```bash
   cd backend
   ```

2. **Create a virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` if needed (default SQLite database is fine for development).

5. **Run the server**:
   ```bash
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to the frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:5173`

## API Documentation

Once the backend server is running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Notes
- `GET /api/notes` - List all notes (with pagination and search)
- `POST /api/notes` - Create a note
- `GET /api/notes/{id}` - Get a note
- `PUT /api/notes/{id}` - Update a note
- `DELETE /api/notes/{id}` - Delete a note
- `POST /api/notes/{note_id}/tags/{tag_id}` - Add tag to note
- `DELETE /api/notes/{note_id}/tags/{tag_id}` - Remove tag from note

### Action Items
- `GET /api/action-items` - List all action items
- `POST /api/action-items` - Create an action item
- `PATCH /api/action-items/{id}` - Update an action item
- `DELETE /api/action-items/{id}` - Delete an action item

### Tags
- `GET /api/tags` - List all tags
- `POST /api/tags` - Create a tag
- `DELETE /api/tags/{id}` - Delete a tag

### Moods
- `GET /api/moods` - List all mood entries
- `POST /api/moods` - Create a mood entry
- `GET /api/moods/stats` - Get weekly/monthly statistics
- `PUT /api/moods/{id}` - Update a mood entry
- `DELETE /api/moods/{id}` - Delete a mood entry

## Database

The application uses SQLite by default (configured in `.env`). The database file `mood_tracker.db` will be created automatically on first run.

## Technologies Used

### Backend
- FastAPI - Modern Python web framework
- SQLAlchemy - SQL toolkit and ORM
- Pydantic - Data validation
- Uvicorn - ASGI server

### Frontend
- Vue 3 - Progressive JavaScript framework
- Vue Router - Official router for Vue.js
- Axios - HTTP client
- Tailwind CSS - Utility-first CSS framework
- Vite - Next generation frontend tooling

## Development

### Backend Development
- The backend uses SQLAlchemy ORM for database operations
- All models include automatic timestamps
- CORS is enabled for frontend communication
- Error handling is implemented throughout

### Frontend Development
- Uses Vue 3 Composition API
- Responsive design with Tailwind CSS
- Dark mode support
- Loading states and error handling
- Empty states for better UX

## Production Deployment

### Backend
1. Set `DATABASE_URL` in `.env` to your production database
2. Run migrations if needed
3. Use a production ASGI server like Gunicorn with Uvicorn workers

### Frontend
1. Build the application: `npm run build`
2. Serve the `dist` directory with a web server like Nginx
3. Update API base URL in `src/api.js` if needed

## License

This project is open source and available for educational purposes.
