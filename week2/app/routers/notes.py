from __future__ import annotations

# Refactored - TODO 3
from typing import List

from fastapi import APIRouter, HTTPException

from .. import db
from ..schemas import NoteCreate, NoteResponse


router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("")
def list_all_notes() -> List[NoteResponse]:
    """Get all notes."""
    # AI Generated - TODO 4
    rows = db.list_notes()
    return [
        NoteResponse(
            id=row["id"],
            content=row["content"],
            created_at=row["created_at"],
        )
        for row in rows
    ]


@router.post("")
def create_note(note: NoteCreate) -> NoteResponse:
    """Create a note using Pydantic schema."""
    content = str(note.content).strip()
    if not content:
        raise HTTPException(status_code=400, detail="content is required")
    note_id = db.insert_note(content)
    note = db.get_note(note_id)
    return NoteResponse(
        id=note["id"],
        content=note["content"],
        created_at=note["created_at"],
    )


@router.get("/{note_id}")
def get_single_note(note_id: int) -> NoteResponse:
    """Fetch a single note by id."""
    row = db.get_note(note_id)
    if row is None:
        raise HTTPException(status_code=404, detail="note not found")
    return NoteResponse(id=row["id"], content=row["content"], created_at=row["created_at"])


