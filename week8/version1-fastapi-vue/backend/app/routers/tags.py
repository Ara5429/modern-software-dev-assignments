from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter(prefix="/api/tags", tags=["tags"])


@router.get("/", response_model=List[schemas.TagResponse])
def get_tags(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tags = db.query(models.Tag).offset(skip).limit(limit).all()
    return tags


@router.get("/{tag_id}", response_model=schemas.TagResponse)
def get_tag(tag_id: int, db: Session = Depends(get_db)):
    tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    return tag


@router.post("/", response_model=schemas.TagResponse)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    # Check if tag with same name already exists
    existing_tag = db.query(models.Tag).filter(models.Tag.name == tag.name).first()
    if existing_tag:
        raise HTTPException(status_code=400, detail="Tag with this name already exists")
    
    db_tag = models.Tag(name=tag.name, color=tag.color)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


@router.put("/{tag_id}", response_model=schemas.TagResponse)
def update_tag(tag_id: int, tag_update: schemas.TagCreate, db: Session = Depends(get_db)):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    # Check if another tag with same name exists
    if tag_update.name != db_tag.name:
        existing_tag = db.query(models.Tag).filter(models.Tag.name == tag_update.name).first()
        if existing_tag:
            raise HTTPException(status_code=400, detail="Tag with this name already exists")
    
    db_tag.name = tag_update.name
    db_tag.color = tag_update.color
    db.commit()
    db.refresh(db_tag)
    return db_tag


@router.delete("/{tag_id}")
def delete_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = db.query(models.Tag).filter(models.Tag.id == tag_id).first()
    if not db_tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    
    db.delete(db_tag)
    db.commit()
    return {"message": "Tag deleted successfully"}
