# AI Generated - TODO 3
from typing import List, Optional

from pydantic import BaseModel


class NoteBase(BaseModel):
    """Base schema for notes."""

    content: str


class NoteCreate(NoteBase):
    """Schema for creating a new note."""

    pass


class NoteResponse(NoteBase):
    """Schema for note responses."""

    id: int
    created_at: str


class ActionItemBase(BaseModel):
    """Base schema for action items."""

    text: str


class ActionItemCreate(ActionItemBase):
    """Schema for creating action items."""

    pass


class ActionItemResponse(ActionItemBase):
    """Schema for action item responses."""

    id: int
    note_id: Optional[int] = None
    done: bool = False
    created_at: str


class ExtractRequest(BaseModel):
    """Schema for extraction request."""

    text: str
    save_note: bool = False


class ExtractResponse(BaseModel):
    """Schema for extraction response."""

    note_id: Optional[int] = None
    items: List[dict]
