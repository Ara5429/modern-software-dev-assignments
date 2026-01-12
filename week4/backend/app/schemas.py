from pydantic import BaseModel


class NoteCreate(BaseModel):
    title: str
    content: str


class NoteRead(BaseModel):
    id: int
    title: str
    content: str

    class Config:
        from_attributes = True


class ActionItemCreate(BaseModel):
    description: str


class ActionItemRead(BaseModel):
    id: int
    description: str
    completed: bool

    class Config:
        from_attributes = True


class TagCreate(BaseModel):
    name: str
    color: str


class TagRead(BaseModel):
    id: int
    name: str
    color: str

    class Config:
        from_attributes = True
