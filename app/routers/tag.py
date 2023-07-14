from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, schemas


router = APIRouter(
    prefix="/tags",
    tags=['Tags']
)

@router.get("/", response_model=List[schemas.TagOut])
def get_tags(db: Session = Depends(get_db)):
    db_tags = db.query(models.Tags).all()
    return db_tags

@router.get("/{recipe_id}", response_model=List[schemas.TagOut])
def get_tag(recipe_id: int, db: Session = Depends(get_db)):
    db_tag = db.query(models.Tags).filter(models.Tags.recipe_id == recipe_id).all()
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag
