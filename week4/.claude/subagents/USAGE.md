# SubAgents Usage Guide

## Overview
SubAgents are specialized AI assistants that work together to implement features using Test-Driven Development (TDD). Each agent has a specific role and expertise.

## Available Agents

### 🧪 TestAgent
- **Role**: Testing specialist
- **Config**: `.claude/subagents/test-agent.md`
- **Expertise**: Writing comprehensive tests, TDD methodology
- **Responsibilities**: Write failing tests first, verify implementations

### ⚙️ CodeAgent
- **Role**: Implementation specialist
- **Config**: `.claude/subagents/code-agent.md`
- **Expertise**: FastAPI, SQLAlchemy, clean code
- **Responsibilities**: Implement features to pass tests, format code

## How It Works

### TDD Workflow with SubAgents:

```
User Request
    ↓
TestAgent (Red Phase)
    → Writes failing tests
    → Documents test scenarios
    → Hands off to CodeAgent
    ↓
CodeAgent (Green Phase)
    → Reviews tests
    → Implements features
    → Formats code
    → Hands back to TestAgent
    ↓
TestAgent (Verification)
    → Runs tests
    → Reports results
    → Suggests fixes (if needed)
    ↓
Done! ✅
```

## Usage Examples

### Example 1: Add UPDATE endpoint for notes

#### Step 1: Invoke TestAgent
```
You: "TestAgent, please write tests for PUT /notes/{id} endpoint that updates a note's title and content."

TestAgent:
🧪 TestAgent here!

I'll write tests for: PUT /notes/{id} - Update note endpoint

Test scenarios:
1. Successfully update note with valid data
2. Update note with partial data (only title or only content)
3. Return 404 when note doesn't exist
4. Return 422 when data is invalid

Working on it...

[Creates backend/tests/test_notes.py with tests]

✅ Tests written!
📁 File: backend/tests/test_notes.py
📊 Test cases: 4
  - Success: 2
  - Error (404): 1
  - Error (422): 1

🔴 Current status: FAILING (as expected in TDD)

🤝 Handing off to CodeAgent for implementation!
```

#### Step 2: Invoke CodeAgent
```
You: "CodeAgent, please implement the update endpoint to pass TestAgent's tests."

CodeAgent:
⚙️ CodeAgent here!

Received tests from TestAgent:
- File: backend/tests/test_notes.py
- Tests: 4 test cases

Implementation plan:
1. Add NoteUpdate schema to schemas.py
2. Add PUT /notes/{id} endpoint to routers/notes.py
3. Handle validation and 404 errors
4. Format code

Starting implementation...

[Implements the feature]

✅ Implementation complete!

📁 Files modified:
  • backend/app/schemas.py - Added NoteUpdate schema
  • backend/app/routers/notes.py - Added update_note endpoint

🎯 Features implemented:
  • PUT /notes/{id} endpoint
  • Partial update support
  • Error handling (404, 422)

🔧 Code formatted with black/ruff

🤝 Handing back to TestAgent for verification!
```

#### Step 3: TestAgent Verification
```
You: "TestAgent, please verify the implementation."

TestAgent:
🧪 Test Verification Results:

Running: pytest backend/tests/test_notes.py::test_update_note* -v

✅ All tests passed! (4/4)

Test results:
  ✅ test_update_note_success
  ✅ test_update_note_partial
  ✅ test_update_note_not_found
  ✅ test_update_note_invalid_data

🎉 Implementation verified! Feature is complete.
```

### Example 2: Add DELETE endpoint

#### Single command approach:
```
You: "I need a DELETE /notes/{id} endpoint. TestAgent, write tests. CodeAgent, implement it. TestAgent, verify."

[Both agents work in sequence]

TestAgent: ✅ Tests written (3 test cases)
CodeAgent: ✅ Implementation complete
TestAgent: ✅ All tests passed! (3/3)
```

### Example 3: Fix failing tests

```
You: "TestAgent, some tests are failing. Please investigate."

TestAgent:
🧪 Running tests...

❌ Tests failed: (2/8)

Failed tests:
- test_search_notes_empty_query: Expected 200, got 500
- test_search_notes_special_chars: SQL error with '%' character

Root cause: search endpoint doesn't handle None or special characters

Suggested fixes:
1. Add null check for query parameter
2. Escape special SQL characters

You: "CodeAgent, please fix these issues."

CodeAgent:
⚙️ Fixing issues...
[Makes fixes]
✅ Complete!

You: "TestAgent, verify the fixes."

TestAgent:
✅ All tests passed! (8/8)
```

## Best Practices

### 1. Always start with TestAgent
```
❌ Bad: "CodeAgent, add a search feature"
✅ Good: "TestAgent, write tests for search feature"
```

### 2. Let agents hand off to each other
```
TestAgent completes → Hands to CodeAgent
CodeAgent completes → Hands to TestAgent
```

### 3. Be specific in requirements
```
❌ Vague: "Add update functionality"
✅ Specific: "Add PUT /notes/{id} that updates title and content, returns 404 if not found"
```

### 4. Verify after implementation
```
Always: TestAgent → CodeAgent → TestAgent (verify)
```

### 5. Use agents for their expertise
```
TestAgent:
  - Write tests
  - Verify implementations
  - Suggest test scenarios

CodeAgent:
  - Implement features
  - Fix bugs
  - Refactor code
```

## Advanced Usage

### Parallel work (independent features):
```
Session 1 (TestAgent): Write tests for tags feature
Session 2 (CodeAgent): Implement users feature (already has tests)
Session 3 (TestAgent): Verify users feature
```

### Iterative refinement:
```
TestAgent: Write basic tests
CodeAgent: Implement
TestAgent: "Tests pass but we need edge cases"
TestAgent: Add more tests (now failing)
CodeAgent: Fix implementation
TestAgent: ✅ All pass
```

### Code review workflow:
```
CodeAgent: Implement feature
TestAgent: Review + write tests
User: "Add this edge case"
TestAgent: Add test for edge case
CodeAgent: Fix implementation
TestAgent: ✅ Verified
```

## Troubleshooting

### Tests won't pass:
1. TestAgent: Review test requirements
2. CodeAgent: Check implementation
3. User: Verify requirements are correct

### Agents confused:
1. Start fresh conversation
2. Be more specific in request
3. Reference existing files explicitly

### Merge conflicts:
1. CodeAgent: Review both implementations
2. Choose best approach
3. TestAgent: Verify merged code

## Integration with Other Tools

### With slash commands:
```
/add-crud Tag "name:str, color:str"  # Generate basic CRUD
TestAgent: Add edge case tests       # Enhance tests
CodeAgent: Handle edge cases          # Improve implementation
```

### With CLAUDE.md:
- Agents automatically follow project conventions
- No need to repeat style rules
- Consistent code across agents

## Success Checklist

Before considering a feature complete:
- ✅ TestAgent wrote comprehensive tests
- ✅ CodeAgent implemented feature
- ✅ TestAgent verified all tests pass
- ✅ Code is formatted (black/ruff)
- ✅ Error handling included
- ✅ Follows project conventions

## Quick Reference

### Invoke TestAgent:
```
"TestAgent, write tests for <feature>"
"TestAgent, verify the implementation"
"TestAgent, add edge case tests for <scenario>"
```

### Invoke CodeAgent:
```
"CodeAgent, implement <feature> to pass tests"
"CodeAgent, fix the failing tests"
"CodeAgent, refactor <module>"
```

### Full workflow:
```
"TestAgent, write tests for <feature>. CodeAgent, implement it. TestAgent, verify."
```