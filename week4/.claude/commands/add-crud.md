# Add CRUD Command

## Purpose
Scaffold a complete CRUD API for a new resource with:
- Database model (SQLAlchemy)
- Pydantic schemas (Create, Read, Update)
- FastAPI router with 5 endpoints (Create, Read All, Read One, Update, Delete)
- Comprehensive tests
- Router registration in main.py

## Usage
```
/add-crud <ResourceName> "<field1:type1, field2:type2, ...>" [options]
```

## Arguments
- `ResourceName`: Singular, PascalCase (e.g., Tag, Comment, Product)
- `Fields`: Comma-separated field definitions
  - Format: `field_name:type`
  - Supported types: `str, int, float, bool, datetime, text`
  - Example: `"name:str, email:str, age:int, active:bool"`

## Field Type Mapping
```
Input Type  → SQLAlchemy Column    → Python Type
str         → String(200)          → str
text        → Text                 → str  (for long content)
int         → Integer              → int
float       → Float                → float
bool        → Boolean              → bool
datetime    → DateTime             → datetime
```

## Steps

### 1. Parse and validate input
- Extract resource name (must be singular, PascalCase)
- Parse field definitions
- Validate field types
- Generate plural form for table name (simple: add 's')
- Generate snake_case variants

Example:
```
Input: Tag "name:str, color:str"
→ Class: Tag
→ Table: tags
→ Router: /tags
→ Files: tags.py, test_tags.py
```

### 2. Update models.py
Add new model class:
```python
class Tag(Base):
    __tablename__ = "tags"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    color = Column(String(200), nullable=False)
```

- Always include `id` field (auto-generated)
- Use appropriate Column types
- Add `nullable=False` for required fields
- Follow existing patterns in the file

### 3. Update schemas.py
Add three schema classes:
```python
class TagCreate(BaseModel):
    """Schema for creating a tag."""
    name: str
    color: str

class TagUpdate(BaseModel):
    """Schema for updating a tag."""
    name: str | None = None
    color: str | None = None

class TagRead(BaseModel):
    """Schema for reading a tag."""
    id: int
    name: str
    color: str
    
    class Config:
        from_attributes = True
```

### 4. Create router file
Create `backend/app/routers/<resource_plural>.py`:

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Tag
from ..schemas import TagCreate, TagRead, TagUpdate

router = APIRouter(prefix="/tags", tags=["tags"])

@router.get("/", response_model=list[TagRead])
def list_items(db: Session = Depends(get_db)) -> list[TagRead]:
    """List all tags."""
    rows = db.execute(select(Tag)).scalars().all()
    return [TagRead.model_validate(row) for row in rows]

@router.post("/", response_model=TagRead, status_code=201)
def create_item(payload: TagCreate, db: Session = Depends(get_db)) -> TagRead:
    """Create a new tag."""
    item = Tag(**payload.model_dump())
    db.add(item)
    db.flush()
    db.refresh(item)
    return TagRead.model_validate(item)

@router.get("/{item_id}", response_model=TagRead)
def get_item(item_id: int, db: Session = Depends(get_db)) -> TagRead:
    """Get a specific tag by ID."""
    item = db.get(Tag, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Tag not found")
    return TagRead.model_validate(item)

@router.put("/{item_id}", response_model=TagRead)
def update_item(
    item_id: int, 
    payload: TagUpdate, 
    db: Session = Depends(get_db)
) -> TagRead:
    """Update a tag."""
    item = db.get(Tag, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    for key, value in payload.model_dump(exclude_unset=True).items():
        setattr(item, key, value)
    
    db.add(item)
    db.flush()
    db.refresh(item)
    return TagRead.model_validate(item)

@router.delete("/{item_id}", status_code=204)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a tag."""
    item = db.get(Tag, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(item)
```

### 5. Register router in main.py
Add import and include_router:
```python
from .routers import tags as tags_router

# In the app setup:
app.include_router(tags_router.router)
```

### 6. Generate tests
Create `backend/tests/test_<resource_plural>.py`:

Generate comprehensive tests:
- `test_create_<resource>` - Create and verify
- `test_list_<resource>s` - List all items
- `test_get_<resource>` - Get specific item
- `test_get_<resource>_not_found` - 404 error
- `test_update_<resource>` - Update item
- `test_update_<resource>_not_found` - Update 404
- `test_delete_<resource>` - Delete item
- `test_delete_<resource>_not_found` - Delete 404

### 7. Update database seed (optional)
Add sample data to `data/seed.sql`:
```sql
INSERT INTO tags (name, color) VALUES
  ('urgent', 'red'),
  ('work', 'blue');
```

### 8. Format and validate
- Run `black` on all modified files
- Run `ruff check --fix`
- Verify imports are correct
- Check for syntax errors
- DO NOT run tests (user will do it)

### 9. Output summary
```
✅ CRUD scaffolding complete for: Tag

📁 Files created/modified:
  • backend/app/models.py (Tag model added)
  • backend/app/schemas.py (TagCreate, TagRead, TagUpdate added)
  • backend/app/routers/tags.py (5 endpoints created)
  • backend/app/main.py (router registered)
  • backend/tests/test_tags.py (8 tests created)
  • data/seed.sql (sample data added)

🌐 API Endpoints:
  • GET    /tags/          - List all tags
  • POST   /tags/          - Create tag
  • GET    /tags/{id}      - Get specific tag
  • PUT    /tags/{id}      - Update tag
  • DELETE /tags/{id}      - Delete tag

🧪 Tests generated: 8
  - Success cases: 5
  - Error cases (404): 3

▶️  Next steps:
  1. Delete data/app.db (if exists)
  2. Restart server: make run
  3. Check OpenAPI docs: http://localhost:8000/docs
  4. Run tests: pytest backend/tests/test_tags.py -v
  5. Add custom business logic if needed

⚠️  Database note:
  Since models changed, you may need to:
  - Delete data/app.db
  - Restart the server (it will recreate tables)
  - Or run: make seed
```

## Safety Notes
- Backs up modified files before changes
- Does NOT modify existing models (only appends)
- Does NOT run database migrations (manual recreate needed)
- Always formats code after generation
- Validates resource name format

## Example Usage

### Basic usage
```
/add-crud Tag "name:str, color:str"
```

### More complex example
```
/add-crud Product "name:str, description:text, price:float, in_stock:bool, created_at:datetime"
```

### User management
```
/add-crud User "username:str, email:str, full_name:str, is_active:bool"
```

## Common Pitfalls to Avoid
- ❌ Don't use plural for ResourceName: `Tags` → use `Tag`
- ❌ Don't forget quotes around fields: `name:str` → use `"name:str"`
- ❌ Don't use reserved words: `id`, `type`, `class`
- ✅ Use singular: `Tag`, `Comment`, `Product`
- ✅ Use PascalCase: `ProductCategory`, not `productcategory`

## Related Commands
- `/generate-tests` - Generate additional tests
- `make seed` - Reset database with new schema
- `make run` - Restart server