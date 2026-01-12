import os
import pytest

from ..app.services.extract import extract_action_items
from week2.app.services.extract import extract_action_items_llm


def test_extract_bullets_and_checkboxes():
    text = """
    Notes from meeting:
    - [ ] Set up database
    * implement API extract endpoint
    1. Write tests
    Some narrative sentence.
    """.strip()

    items = extract_action_items(text)
    assert "Set up database" in items
    assert "implement API extract endpoint" in items
    assert "Write tests" in items


@pytest.mark.integration  # AI Generated - TODO 2
def test_extract_llm_bullets():
    """Ensure bullet markers are captured as separate items."""
    text = "- Set up database\n* Write tests\n• Deploy app"

    items = extract_action_items_llm(text)

    assert len(items) >= 3
    assert any("Set up database" in item for item in items)
    assert any("Write tests" in item for item in items)
    assert any("Deploy app" in item for item in items)


@pytest.mark.integration  # AI Generated - TODO 2
def test_extract_llm_keywords():
    """Strip TODO/Action/Next prefixes while extracting tasks."""
    text = "TODO: Fix bug\nAction: Review code\nNext: Deploy"

    items = extract_action_items_llm(text)

    assert len(items) >= 3
    assert any("Fix bug" in item for item in items)
    assert any("Review code" in item for item in items)
    assert any("Deploy" in item for item in items)


@pytest.mark.integration  # AI Generated - TODO 2
def test_extract_llm_checkboxes():
    """Handle checkbox syntax and drop markers."""
    text = "[ ] Configure CI\n[x] Setup env\n[ ] Write docs"

    items = extract_action_items_llm(text)

    assert len(items) >= 1
    assert all(not item.strip().startswith(("[ ]", "[x]", "[X]")) for item in items)
    assert any("Configure CI" in item for item in items)
    assert any("Write docs" in item for item in items)


@pytest.mark.integration  # AI Generated - TODO 2
def test_extract_llm_empty():
    """Return empty list for empty input."""
    text = ""

    items = extract_action_items_llm(text)

    assert items == []


@pytest.mark.integration  # AI Generated - TODO 2
def test_extract_llm_narrative():
    """Extract tasks from narrative sentences."""
    text = (
        "We need to set up the database. "
        "The team should implement the API. "
        "Don't forget to write tests."
    )

    items = extract_action_items_llm(text)

    assert len(items) >= 1
    assert any("set up the database" in item.lower() for item in items)
    assert any("implement the api" in item.lower() for item in items)


@pytest.mark.integration  # AI Generated - TODO 2
def test_extract_llm_mixed():
    """Work with mixed bullet, keyword, and narrative inputs."""
    text = "- [ ] Set up DB\nTODO: Write tests\nWe should deploy to staging"

    items = extract_action_items_llm(text)

    assert len(items) >= 2
    assert any("Set up DB" in item for item in items)
    assert any("Write tests" in item for item in items)
    assert any("deploy to staging" in item.lower() for item in items)
