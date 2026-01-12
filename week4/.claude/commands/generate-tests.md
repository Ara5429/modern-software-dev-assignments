# Generate Tests Command

## Purpose
Automatically generate comprehensive pytest test cases for FastAPI routers.
Analyzes the router file and creates tests for all endpoints including:
- Success cases (200, 201 responses)
- Error cases (404, 400, 422 validation errors)
- Edge cases (empty data, invalid IDs)

## Usage
```
/generate-tests <router_file_path> [options]
```

## Arguments
- `$ARGUMENTS`: Path to the router file (e.g., `backend/app/routers/notes.py`)
- Optional flags:
  - `--overwrite`: Overwrite existing test file
  - `--append`: Append to existing test file

## Steps

### 1. Analyze the router file
- Read the specified router file
- Identify all endpoints (GET, POST, PUT, DELETE, PATCH)
- Extract route paths, parameters, request/response models
- Note any dependencies (database, auth, etc.)

### 2. Determine test file location
- Router: `backend/app/routers/X.py`
- Test file: `backend/tests/test_X.py`
- Check if test file already exists

### 3. Generate test cases
For each endpoint, generate tests for:

**Success cases:**
- Valid request with expected response
- Correct status codes (200, 201, 204)
- Response model validation

**Error cases:**
- 404 Not Found (invalid IDs)
- 400 Bad Request (invalid data)
- 422 Validation Error (schema violations)

**Edge cases:**
- Empty strings
- Null values
- Boundary values (min/max)
- SQL injection attempts (if applicable)

### 4. Follow project conventions
- Use pytest fixtures from `conftest.py`
- Use `TestClient` for API testing
- Follow naming convention: `test_<action>_<resource>_<scenario>`
- Add docstrings for complex test cases
- Use type hints

### 5. Ensure test isolation
- Each test should be independent
- Use the test database (from fixtures)
- No side effects between tests
- Clean up is handled by fixtures

### 6. Format and validate
- Run `black` on the generated test file
- Run `ruff check --fix`
- Verify tests are syntactically correct
- DO NOT run the tests yet (user will run them)

### 7. Output summary
Provide:
- Path to generated test file
- Number of test cases created
- List of tested endpoints
- Command to run tests: `make test` or `pytest backend/tests/test_X.py`
- Next steps for the user

## Example Output
```
✅ Generated test file: backend/tests/test_notes.py

📊 Summary:
- Total test cases: 8
- Endpoints tested: 4
  • GET /notes/ (list_notes)
  • POST /notes/ (create_note)
  • GET /notes/search/ (search_notes)
  • GET /notes/{note_id} (get_note)

🧪 Test coverage:
- Success cases: 4
- Error cases (404): 1
- Error cases (validation): 2
- Edge cases: 1

▶️  Run tests:
  make test
  # or
  pytest backend/tests/test_notes.py -v

📝 Next steps:
1. Review generated tests
2. Add any custom test cases
3. Run tests to verify
4. Commit changes
```

## Safety Notes
- Does NOT overwrite existing tests by default
- Always formats code after generation
- Does NOT run tests automatically (user controls execution)
- Creates backup if overwriting (.bak file)

## Example Usage

### Basic usage
```
/generate-tests backend/app/routers/notes.py
```

### With overwrite
```
/generate-tests backend/app/routers/action_items.py --overwrite
```

### Multiple routers
```
/generate-tests backend/app/routers/notes.py
/generate-tests backend/app/routers/action_items.py
```

## Related Commands
- `/tests` - Run tests with coverage
- `make test` - Run all tests
- `make format` - Format code