from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List


class TagBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)
    color: Optional[str] = Field("#3B82F6", pattern=r"^#[0-9A-Fa-f]{6}$")


class TagCreate(TagBase):
    pass


class TagResponse(TagBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class MoodEntryBase(BaseModel):
    mood: str = Field(..., pattern="^(happy|neutral|sad|angry|tired)$")
    date: Optional[datetime] = None


class MoodEntryCreate(MoodEntryBase):
    pass  # Removed note_id - mood is independent now


class MoodEntryUpdate(BaseModel):
    mood: Optional[str] = Field(None, pattern="^(happy|neutral|sad|angry|tired)$")


class MoodEntryResponse(MoodEntryBase):
    id: int
    date: datetime
    created_at: datetime

    class Config:
        from_attributes = True


class NoteBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: Optional[str] = None
    mood_id: Optional[int] = None


class NoteCreate(NoteBase):
    tag_ids: Optional[List[int]] = []


class NoteUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = None
    mood_id: Optional[int] = None
    tag_ids: Optional[List[int]] = None


class NoteResponse(NoteBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[TagResponse] = []
    mood_entry: Optional[MoodEntryResponse] = None

    class Config:
        from_attributes = True


class ActionItemBase(BaseModel):
    description: str = Field(..., min_length=1, max_length=500)
    completed: Optional[bool] = False


class ActionItemCreate(ActionItemBase):
    pass


class ActionItemUpdate(BaseModel):
    description: Optional[str] = Field(None, min_length=1, max_length=500)
    completed: Optional[bool] = None


class ActionItemResponse(ActionItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
