# Week 4 Developer Command Center

## Project Overview
FastAPI-based full-stack application for managing notes and action items.
- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Frontend**: Vanilla JS (no build step)
- **Testing**: pytest
- **Code Quality**: black + ruff

## Quick Start
```bash
# From week4/ directory
conda activate cs146s
make run          # Start server (localhost:8000)
make test         # Run all tests
make format       # Format with black + ruff
make lint         # Check code quality
make seed         # Reset database
```

## Project Structure
```
backend/
  app/
    main.py          # FastAPI app entry point
    models.py        # SQLAlchemy models (Note, ActionItem)
    schemas.py       # Pydantic schemas for validation
    db.py            # Database connection & session
    routers/         # API endpoints
      notes.py       # Notes CRUD
      action_items.py # Action items CRUD
    services/
      extract.py     # Business logic (extract action items)
  tests/
    conftest.py      # pytest fixtures
    test_*.py        # Test files
frontend/
  index.html         # Main UI
  app.js            # Vanilla JS
  styles.css        # Minimal CSS
data/
  app.db            # SQLite database
  seed.sql          # Initial data
```

## Development Workflow

### When adding a new feature:
1. **Write failing test first** (TDD approach)
2. **Implement the feature**
3. **Run tests**: `make test`
4. **Format code**: `make format`
5. **Check lint**: `make lint`

### When adding a new endpoint:
1. Add route in `backend/app/routers/`
2. Update schemas in `schemas.py` if needed
3. Write tests in `backend/tests/`
4. Update API docs if needed

### When modifying database:
1. Update models in `models.py`
2. Update seed in `data/seed.sql`
3. Delete `data/app.db` and restart server
4. Run `make seed` to recreate

## Code Style Rules
- **Formatting**: Use `black` (line length 100)
- **Linting**: Use `ruff` with fixes
- **Type Hints**: Prefer type hints for function signatures
- **Imports**: Group stdlib, third-party, local
- **Docstrings**: Not required for simple functions

## Safe Commands
✅ `make run` - Start development server
✅ `make test` - Run tests (uses temporary DB)
✅ `make format` - Auto-format code
✅ `make lint` - Check code quality
✅ `make seed` - Reset database safely
✅ `pytest backend/tests` - Run specific tests
✅ `black .` - Format all Python files
✅ `ruff check . --fix` - Fix linting issues

## Commands to Avoid
❌ `rm -rf data/` - Don't delete data folder
❌ `pip install` without venv - Use conda env
❌ Direct SQL execution - Use SQLAlchemy
❌ Editing `app.db` manually - Use seed.sql

## Testing Guidelines
- Tests use **temporary database** (conftest.py)
- Use FastAPI `TestClient` for API tests
- Test both success and error cases
- Verify status codes and response structure
- Clean up is automatic (fixtures)

## Common Tasks
See `docs/TASKS.md` for detailed task list including:
- Enable pre-commit hooks
- Add search endpoints
- Complete action item flow
- Improve extraction logic
- CRUD enhancements
- Request validation

## API Endpoints
- `GET /` - Frontend UI
- `GET /docs` - OpenAPI documentation
- `GET /notes/` - List all notes
- `POST /notes/` - Create note
- `GET /notes/search/?q=query` - Search notes
- `GET /notes/{id}` - Get specific note
- `GET /action-items/` - List action items
- `POST /action-items/` - Create action item
- `PUT /action-items/{id}/complete` - Mark as complete

## Notes for AI Assistants
- Always run tests after code changes
- Use type hints from schemas.py
- Follow existing patterns in routers/
- Don't break existing tests
- Prefer SQLAlchemy queries over raw SQL
- Keep frontend simple (no frameworks)