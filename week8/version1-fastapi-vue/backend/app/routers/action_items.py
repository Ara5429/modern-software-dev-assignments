from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, models
from app.database import get_db

router = APIRouter(prefix="/api/action-items", tags=["action-items"])


@router.get("/", response_model=List[schemas.ActionItemResponse])
def get_action_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    action_items = db.query(models.ActionItem).offset(skip).limit(limit).all()
    return action_items


@router.get("/{item_id}", response_model=schemas.ActionItemResponse)
def get_action_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.ActionItem).filter(models.ActionItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Action item not found")
    return item


@router.post("/", response_model=schemas.ActionItemResponse)
def create_action_item(item: schemas.ActionItemCreate, db: Session = Depends(get_db)):
    db_item = models.ActionItem(
        description=item.description,
        completed=item.completed
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@router.put("/{item_id}", response_model=schemas.ActionItemResponse)
def update_action_item(item_id: int, item_update: schemas.ActionItemUpdate, db: Session = Depends(get_db)):
    db_item = db.query(models.ActionItem).filter(models.ActionItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Action item not found")
    
    if item_update.description is not None:
        db_item.description = item_update.description
    if item_update.completed is not None:
        db_item.completed = item_update.completed
    
    db.commit()
    db.refresh(db_item)
    return db_item


@router.delete("/{item_id}")
def delete_action_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(models.ActionItem).filter(models.ActionItem.id == item_id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="Action item not found")
    
    db.delete(db_item)
    db.commit()
    return {"message": "Action item deleted successfully"}
