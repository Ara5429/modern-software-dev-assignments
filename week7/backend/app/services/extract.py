import re
from typing import NotRequired, TypedDict


class ActionItem(TypedDict):
    """Structured action item extracted from text.

    Attributes:
        text: The original line text
        priority: Priority level (P0, P1, P2, P3, high, medium, low)
        due_date: Due date in various formats
        assignee: Assigned person's username or name
    """

    text: str
    priority: NotRequired[str | None]
    due_date: NotRequired[str | None]
    assignee: NotRequired[str | None]


def extract_action_items(text: str) -> list[ActionItem]:
    """Extract action items from text with sophisticated pattern recognition.

    Detects action items using multiple patterns:
    - TODO:/ACTION: prefixes
    - Lines ending with "!"
    - Action verbs (implement, fix, create, etc.)
    - Checkbox format [ ]

    Extracts structured information:
    - Priority: Explicit (P0-P3, high/medium/low) or implicit (!!!=P0, !!=P1, !=P2)
    - Due dates: YYYY-MM-DD, MM/DD/YYYY, MM/DD, or natural language
    - Assignee: @username or "assigned to:" patterns

    Args:
        text: Input text to extract action items from

    Returns:
        List of ActionItem dictionaries with extracted information

    Examples:
        >>> text = "TODO: Fix bug P0 @john"
        >>> items = extract_action_items(text)
        >>> items[0]["text"]
        'TODO: Fix bug P0 @john'
        >>> items[0]["priority"]
        'P0'
        >>> items[0]["assignee"]
        'john'

        >>> text = "Deploy by Friday!!!"
        >>> items = extract_action_items(text)
        >>> items[0]["priority"]
        'P0'
        >>> items[0]["due_date"]
        'by Friday'

        >>> text = "[ ] Review PR assigned to: alice"
        >>> items = extract_action_items(text)
        >>> items[0]["assignee"]
        'alice'
    """
    if not text or not text.strip():
        return []

    lines = [line.strip("- ") for line in text.splitlines() if line.strip()]
    results: list[ActionItem] = []

    # Action verbs that indicate actionable items
    action_verbs = [
        "implement",
        "fix",
        "create",
        "update",
        "review",
        "deploy",
        "test",
        "refactor",
        "build",
        "setup",
        "configure",
        "investigate",
        "resolve",
    ]

    for line in lines:
        normalized = line.lower().strip()

        # Check if line is an action item
        is_action_item = False

        # Check for TODO:/ACTION: prefix
        if normalized.startswith("todo:") or normalized.startswith("action:"):
            is_action_item = True

        # Check for checkbox format [ ] or [x]
        elif re.match(r"^\s*\[[\sxX]\]", line):
            is_action_item = True

        # Check for lines ending with !
        elif line.rstrip().endswith("!"):
            is_action_item = True

        # Check for action verbs at start of line
        else:
            for verb in action_verbs:
                if normalized.startswith(verb + " ") or normalized.startswith(verb + ":"):
                    is_action_item = True
                    break

        if not is_action_item:
            continue

        # Extract structured information
        item: ActionItem = {"text": line}

        # Extract priority
        priority = _extract_priority(line)
        if priority:
            item["priority"] = priority

        # Extract due date
        due_date = _extract_due_date(line)
        if due_date:
            item["due_date"] = due_date

        # Extract assignee
        assignee = _extract_assignee(line)
        if assignee:
            item["assignee"] = assignee

        results.append(item)

    return results


def _extract_priority(text: str) -> str | None:
    """Extract priority from text.

    Explicit priorities: P0, P1, P2, P3, high, medium, low (case-insensitive)
    Implicit priorities: !!! = P0, !! = P1, ! = P2
    """
    # Check for explicit priority patterns
    priority_patterns = [
        (r"\bP0\b", "P0"),
        (r"\bP1\b", "P1"),
        (r"\bP2\b", "P2"),
        (r"\bP3\b", "P3"),
        (r"\bhigh\b", "high"),
        (r"\bmedium\b", "medium"),
        (r"\blow\b", "low"),
    ]

    text_lower = text.lower()
    for pattern, priority in priority_patterns:
        if re.search(pattern, text_lower, re.IGNORECASE):
            return priority

    # Check for implicit priority (exclamation marks at end)
    exclamation_count = len(text.rstrip()) - len(text.rstrip().rstrip("!"))
    if exclamation_count >= 3:
        return "P0"
    elif exclamation_count == 2:
        return "P1"
    elif exclamation_count == 1:
        return "P2"

    return None


def _extract_due_date(text: str) -> str | None:
    """Extract due date from text.

    Supports:
    - YYYY-MM-DD format (e.g., 2024-12-31)
    - MM/DD/YYYY format (e.g., 12/31/2024)
    - MM/DD format (e.g., 12/31)
    - Natural language: "by Friday", "due Monday", etc.
    """
    # YYYY-MM-DD format
    date_pattern = r"\b(\d{4}-\d{1,2}-\d{1,2})\b"
    match = re.search(date_pattern, text)
    if match:
        return match.group(1)

    # MM/DD/YYYY format
    date_pattern = r"\b(\d{1,2}/\d{1,2}/\d{4})\b"
    match = re.search(date_pattern, text)
    if match:
        return match.group(1)

    # MM/DD format
    date_pattern = r"\b(\d{1,2}/\d{1,2})\b"
    match = re.search(date_pattern, text)
    if match:
        return match.group(1)

    # Natural language patterns
    natural_patterns = [
        r"\bby\s+([A-Za-z]+day)\b",  # by Friday, by Monday
        r"\bdue\s+([A-Za-z]+day)\b",  # due Monday
        r"\bby\s+([A-Za-z]+\s+\d{1,2})",  # by December 31
        r"\bdue\s+([A-Za-z]+\s+\d{1,2})",  # due December 31
    ]

    for pattern in natural_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(0).strip()

    return None


def _extract_assignee(text: str) -> str | None:
    """Extract assignee from text.

    Supports:
    - @username format
    - "assigned to: name"
    - "owner: name"
    - "assignee: name"
    """
    # @username format
    username_pattern = r"@([a-zA-Z0-9_-]+)"
    match = re.search(username_pattern, text)
    if match:
        return match.group(1)

    # "assigned to:" pattern
    assigned_patterns = [
        r"assigned\s+to:\s*([^\s,]+)",
        r"owner:\s*([^\s,]+)",
        r"assignee:\s*([^\s,]+)",
    ]

    for pattern in assigned_patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()

    return None
