from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app import schemas, models
from app.database import get_db

router = APIRouter(prefix="/api/notes", tags=["notes"])


@router.get("/", response_model=List[schemas.NoteResponse])
def get_notes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    notes = db.query(models.Note).offset(skip).limit(limit).all()
    return notes


@router.get("/{note_id}", response_model=schemas.NoteResponse)
def get_note(note_id: int, db: Session = Depends(get_db)):
    note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.post("/", response_model=schemas.NoteResponse)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = models.Note(
        title=note.title,
        content=note.content,
        mood_id=note.mood_id
    )
    
    # Add tags if provided
    if note.tag_ids:
        tags = db.query(models.Tag).filter(models.Tag.id.in_(note.tag_ids)).all()
        db_note.tags = tags
    
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


@router.put("/{note_id}", response_model=schemas.NoteResponse)
def update_note(note_id: int, note_update: schemas.NoteUpdate, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    if note_update.title is not None:
        db_note.title = note_update.title
    if note_update.content is not None:
        db_note.content = note_update.content
    if note_update.mood_id is not None:
        db_note.mood_id = note_update.mood_id
    
    # Update tags if provided
    if note_update.tag_ids is not None:
        tags = db.query(models.Tag).filter(models.Tag.id.in_(note_update.tag_ids)).all()
        db_note.tags = tags
    
    db_note.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_note)
    return db_note


@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    db_note = db.query(models.Note).filter(models.Note.id == note_id).first()
    if not db_note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    db.delete(db_note)
    db.commit()
    return {"message": "Note deleted successfully"}
