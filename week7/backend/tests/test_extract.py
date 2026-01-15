from backend.app.services.extract import extract_action_items


def test_extract_basic_patterns():
    """Test original TODO:/ACTION: patterns and lines ending with !"""
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert len(items) == 3
    
    # Check that items are dictionaries with 'text' key
    texts = [item["text"] for item in items]
    assert "TODO: write tests" in texts
    assert "ACTION: review PR" in texts
    assert "Ship it!" in texts
    
    # Verify all items have text field
    for item in items:
        assert "text" in item
        assert isinstance(item["text"], str)


def test_extract_with_priority():
    """Test priority detection: explicit (P0-P3, high/medium/low) and implicit (!, !!, !!!)"""
    text = """
    TODO: Critical bug P0
    ACTION: Important task P1
    Fix this P2
    TODO: Low priority P3
    Fix high priority item
    Update medium priority task
    Review low priority code
    Urgent!!!
    Important!!
    Normal!
    """.strip()
    items = extract_action_items(text)
    assert len(items) == 10
    
    # Verify priorities are extracted
    priorities = [item.get("priority") for item in items if "priority" in item]
    assert "P0" in priorities
    assert "P1" in priorities
    assert "P2" in priorities
    assert "P3" in priorities

def test_extract_with_due_date():
    """Test due date extraction in various formats"""
    text = """
    TODO: Task due 2024-12-31
    ACTION: Complete by 12/31/2024
    Fix bug by 12/31
    Deploy by Friday
    Review due Monday
    Update by December
    """.strip()
    items = extract_action_items(text)
    assert len(items) == 6
    
    # Verify due dates are extracted
    due_dates = [item.get("due_date") for item in items if "due_date" in item]
    assert len(due_dates) >= 5
    assert any("2024-12-31" in str(d) for d in due_dates)
    assert any("Friday" in str(d) for d in due_dates)


def test_extract_with_assignee():
    """Test assignee extraction: @username, assigned to:, owner:, assignee:"""
    text = """
    TODO: Fix bug @john
    ACTION: Review PR assigned to: alice
    Deploy owner: bob
    Test assignee: charlie
    """.strip()
    items = extract_action_items(text)
    assert len(items) == 4
    
    # Find items by text and verify assignees
    assignees = {item["text"]: item.get("assignee") for item in items}
    
    assert assignees["TODO: Fix bug @john"] == "john"
    assert assignees["ACTION: Review PR assigned to: alice"] == "alice"
    assert assignees["Deploy owner: bob"] == "bob"
    assert assignees["Test assignee: charlie"] == "charlie"


def test_extract_action_verbs():
    """Test detection of action verbs at start of line"""
    text = """
    implement new feature
    fix critical bug
    create documentation
    update dependencies
    review code changes
    deploy to production
    test new functionality
    refactor old code
    build new system
    setup environment
    configure settings
    investigate issue
    resolve conflict
    """.strip()
    items = extract_action_items(text)
    assert len(items) == 13
    
    # Verify all action verbs are detected
    texts = [item["text"] for item in items]
    assert "implement new feature" in texts
    assert "fix critical bug" in texts
    assert "create documentation" in texts
    assert "update dependencies" in texts
    assert "review code changes" in texts
    assert "deploy to production" in texts
    assert "test new functionality" in texts
    assert "refactor old code" in texts
    assert "build new system" in texts
    assert "setup environment" in texts
    assert "configure settings" in texts
    assert "investigate issue" in texts
    assert "resolve conflict" in texts


def test_extract_combined_metadata():
    """Test extraction of multiple metadata fields in one line"""
    text = """
    TODO: Fix bug P0 @john by Friday
    ACTION: Deploy high assigned to: alice 2024-12-31
    implement feature P1 @bob due Monday!!!
    """.strip()
    items = extract_action_items(text)
    assert len(items) == 3
    
    # Verify first item has all fields
    item1 = next(item for item in items if "Fix bug" in item["text"])
    assert item1["text"] == "TODO: Fix bug P0 @john by Friday"
    assert item1.get("priority") == "P0"
    assert item1.get("assignee") == "john"
    assert item1.get("due_date") == "by Friday"
    
    # Verify second item
    item2 = next(item for item in items if "Deploy" in item["text"])
    assert item2["text"] == "ACTION: Deploy high assigned to: alice 2024-12-31"
    assert item2.get("priority") == "high"
    assert item2.get("assignee") == "alice"
    assert item2.get("due_date") == "2024-12-31"
    
    # Verify third item (implicit priority from !!!)
    item3 = next(item for item in items if "implement feature" in item["text"])
    assert item3["text"] == "implement feature P1 @bob due Monday!!!"
    # P1 explicit takes precedence over !!! implicit
    assert item3.get("priority") == "P1"
    assert item3.get("assignee") == "bob"
    assert item3.get("due_date") == "due Monday"


def test_extract_empty_text():
    """Test handling of empty input"""
    assert extract_action_items("") == []
    assert extract_action_items("   ") == []
    assert extract_action_items("\n\n\n") == []


def test_extract_no_action_items():
    """Test text with no action items"""
    text = """
    This is just a regular note.
    It doesn't have any action items.
    Just some text here.
    """.strip()
    items = extract_action_items(text)
    assert len(items) == 0


def test_extract_checklist_format():
    """Test checkbox format [ ] and [x] patterns"""
    text = """
    [ ] Unchecked task
    [x] Completed task
    [X] Another completed task
    [ ] TODO: Task with prefix
    [ ] Fix bug!
    """.strip()
    items = extract_action_items(text)
    assert len(items) == 5
    
    # Verify all checkbox items are detected
    texts = [item["text"] for item in items]
    assert "[ ] Unchecked task" in texts
    assert "[x] Completed task" in texts
    assert "[X] Another completed task" in texts
    assert "[ ] TODO: Task with prefix" in texts
    assert "[ ] Fix bug!" in texts
    
    # Verify checkbox items can have metadata
    item_with_prefix = next(item for item in items if "TODO:" in item["text"])
    assert item_with_prefix["text"] == "[ ] TODO: Task with prefix"
    
    item_with_exclamation = next(item for item in items if "Fix bug!" in item["text"])
    assert item_with_exclamation["text"] == "[ ] Fix bug!"
    assert item_with_exclamation.get("priority") == "P2"


def test_extract_action_items():
    """Legacy test for backward compatibility"""
    text = """
    This is a note
    - TODO: write tests
    - ACTION: review PR
    - Ship it!
    Not actionable
    """.strip()
    items = extract_action_items(text)
    assert len(items) == 3
    
    # Check that items are dictionaries with 'text' key
    texts = [item["text"] for item in items]
    assert "TODO: write tests" in texts
    assert "ACTION: review PR" in texts
    assert "Ship it!" in texts

