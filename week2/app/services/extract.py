from __future__ import annotations

import os
import re
from typing import List
import json
from typing import Any
from ollama import chat
from dotenv import load_dotenv

load_dotenv()

BULLET_PREFIX_PATTERN = re.compile(r"^\s*([-*•]|\d+\.)\s+")
KEYWORD_PREFIXES = (
    "todo:",
    "action:",
    "next:",
)


def _is_action_line(line: str) -> bool:
    stripped = line.strip().lower()
    if not stripped:
        return False
    if BULLET_PREFIX_PATTERN.match(stripped):
        return True
    if any(stripped.startswith(prefix) for prefix in KEYWORD_PREFIXES):
        return True
    if "[ ]" in stripped or "[todo]" in stripped:
        return True
    return False


def extract_action_items(text: str) -> List[str]:
    lines = text.splitlines()
    extracted: List[str] = []
    for raw_line in lines:
        line = raw_line.strip()
        if not line:
            continue
        if _is_action_line(line):
            cleaned = BULLET_PREFIX_PATTERN.sub("", line)
            cleaned = cleaned.strip()
            # Trim common checkbox markers
            cleaned = cleaned.removeprefix("[ ]").strip()
            cleaned = cleaned.removeprefix("[todo]").strip()
            extracted.append(cleaned)
    # Fallback: if nothing matched, heuristically split into sentences and pick imperative-like ones
    if not extracted:
        sentences = re.split(r"(?<=[.!?])\s+", text.strip())
        for sentence in sentences:
            s = sentence.strip()
            if not s:
                continue
            if _looks_imperative(s):
                extracted.append(s)
    # Deduplicate while preserving order
    seen: set[str] = set()
    unique: List[str] = []
    for item in extracted:
        lowered = item.lower()
        if lowered in seen:
            continue
        seen.add(lowered)
        unique.append(item)
    return unique


def extract_action_items_llm(text: str) -> List[str]:
    # AI Generated - TODO 1 (Revised)
    import re

    # For fallback cleaning
    def _deep_clean(item: str) -> str:
        """
        Clean action item text:
        - Remove bullets (-, *, •), numbered lists (1.), ellipsis
        - Remove common prefixes (TODO, Action, Next, case-insensitive, with or without colon)
        - Preserve checkbox markers [ ] and [x]/[X] for deduplication purpose, but then remove
        - Clean up whitespace
        """
        cleaned = item

        # Remove bullet/numbered markers
        cleaned = re.sub(r"^\s*([-*•]|\d+\.)\s*", "", cleaned)

        # Remove checkbox prefix, both unchecked and checked ([ ] or [x]/[X]), at start of line
        cleaned = re.sub(r"^\s*\[( |x|X)\]\s*", "", cleaned)

        # Remove common keyword prefixes (e.g., TODO, Action, Next)
        cleaned = re.sub(r"^(TODO|Action|Next):?\s*", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"^(TODO|Action|Next):?\s*", "", cleaned, flags=re.IGNORECASE)

        # Remove ellipsis
        cleaned = cleaned.replace("...", "")

        # Remove whitespace
        cleaned = cleaned.strip()
        return cleaned

    try:
        response = chat(
            model="llama3.1:8b",
            messages=[
                {
                    "role": "system",
                    "content": 'You are an AI that extracts action items. Return only a JSON array of clean task strings. Example: ["task1", "task2"]',
                },
                {
                    "role": "user",
                    "content": f"Extract all actionable tasks from this text as a JSON array:\n\n{text}",
                },
            ],
            format="json",
            options={"temperature": 0.0},
        )
        raw_content = response.get("message", {}).get("content", "")
        print("=" * 60)
        print("INPUT TEXT:")
        print(text)
        print("-" * 60)
        print("RAW LLM RESPONSE:")
        print(raw_content)
        print("=" * 60)
        content = raw_content.strip()

        # Remove common Markdown JSON fences
        if content.startswith("```"):
            content = content.strip("`")
            if content.lower().startswith("json"):
                content = content[4:].strip()

        # Robust JSON parsing
        try:
            parsed: Any = json.loads(content)
        except Exception:
            parsed = None

        items: List[str] = []
        if isinstance(parsed, list):
            items = parsed
        elif isinstance(parsed, dict):
            # Try to find a single key with a list value
            for v in parsed.values():
                if isinstance(v, list):
                    items = v
                    break
        if not items:
            # As last resort, try splitting by line
            lines = content.splitlines()
            for line in lines:
                s = line.strip()
                if s.startswith("-") or s.startswith("*") or s.startswith("•") or re.match(r"\d+\.", s):
                    s = re.sub(r"^([-*•]|\d+\.)\s*", "", s)
                if s:
                    items.append(s)

        cleaned_items: List[str] = []
        for item in items:
            if not isinstance(item, str):
                continue
            clean = _deep_clean(item)
            # Require >= 3 chars
            if len(clean) >= 3:
                cleaned_items.append(clean)
        return cleaned_items

    except Exception as e:
        print(f"❌ LLM extraction error: {e}")
        print(f"❌ Error type: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        print("⚠️ Falling back to heuristic extraction")
        # Fall back to heuristic extraction on any failure
        return extract_action_items(text)


def _looks_imperative(sentence: str) -> bool:
    words = re.findall(r"[A-Za-z']+", sentence)
    if not words:
        return False
    first = words[0]
    # Crude heuristic: treat these as imperative starters
    imperative_starters = {
        "add",
        "create",
        "implement",
        "fix",
        "update",
        "write",
        "check",
        "verify",
        "refactor",
        "document",
        "design",
        "investigate",
    }
    return first.lower() in imperative_starters
