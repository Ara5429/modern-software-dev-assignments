from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from sqlalchemy.exc import IntegrityError
from typing import List
from datetime import datetime, timedelta
from app import schemas, models
from app.database import get_db

router = APIRouter(prefix="/api/moods", tags=["moods"])

VALID_MOODS = ["happy", "neutral", "sad", "angry", "tired"]


@router.get("/", response_model=List[schemas.MoodEntryResponse])
def get_mood_entries(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    entries = db.query(models.MoodEntry).order_by(models.MoodEntry.date.desc()).offset(skip).limit(limit).all()
    return entries


@router.get("/weekly", response_model=List[schemas.MoodEntryResponse])
def get_weekly_moods(db: Session = Depends(get_db)):
    """Get mood entries from the last 7 days"""
    week_ago = datetime.utcnow() - timedelta(days=7)
    entries = db.query(models.MoodEntry).filter(
        models.MoodEntry.date >= week_ago
    ).order_by(models.MoodEntry.date.asc()).all()
    return entries


@router.get("/stats/weekly")
def get_weekly_mood_stats(db: Session = Depends(get_db)):
    """Get mood statistics for the last 7 days grouped by mood"""
    week_ago = datetime.utcnow() - timedelta(days=7)
    stats = db.query(
        models.MoodEntry.mood,
        func.count(models.MoodEntry.id).label('count')
    ).filter(
        models.MoodEntry.date >= week_ago
    ).group_by(models.MoodEntry.mood).all()
    
    return {mood: count for mood, count in stats}


@router.get("/{mood_id}", response_model=schemas.MoodEntryResponse)
def get_mood_entry(mood_id: int, db: Session = Depends(get_db)):
    entry = db.query(models.MoodEntry).filter(models.MoodEntry.id == mood_id).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Mood entry not found")
    return entry


@router.post("/", response_model=schemas.MoodEntryResponse)
def create_mood_entry(mood: schemas.MoodEntryCreate, db: Session = Depends(get_db)):
    if mood.mood not in VALID_MOODS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid mood. Must be one of: {', '.join(VALID_MOODS)}"
        )
    
    try:
        db_mood = models.MoodEntry(
            mood=mood.mood,
            date=mood.date or datetime.utcnow()
        )
        db.add(db_mood)
        db.commit()
        db.refresh(db_mood)
        return db_mood
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="A mood entry already exists for this date"
        )


@router.put("/{mood_id}", response_model=schemas.MoodEntryResponse)
def update_mood_entry(mood_id: int, mood_update: schemas.MoodEntryCreate, db: Session = Depends(get_db)):
    db_mood = db.query(models.MoodEntry).filter(models.MoodEntry.id == mood_id).first()
    if not db_mood:
        raise HTTPException(status_code=404, detail="Mood entry not found")
    
    if mood_update.mood not in VALID_MOODS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid mood. Must be one of: {', '.join(VALID_MOODS)}"
        )
    
    db_mood.mood = mood_update.mood
    if mood_update.date:
        db_mood.date = mood_update.date
    
    db.commit()
    db.refresh(db_mood)
    return db_mood


@router.delete("/{mood_id}")
def delete_mood_entry(mood_id: int, db: Session = Depends(get_db)):
    db_mood = db.query(models.MoodEntry).filter(models.MoodEntry.id == mood_id).first()
    if not db_mood:
        raise HTTPException(status_code=404, detail="Mood entry not found")
    
    db.delete(db_mood)
    db.commit()
    return {"message": "Mood entry deleted successfully"}
