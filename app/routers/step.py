from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, schemas


router = APIRouter(
    prefix="/steps",
    tags=['Step']
)

@router.get("/", response_model=List[schemas.StepOut])
def get_steps(db: Session = Depends(get_db)):
    db_steps = db.query(models.Step).all()
    return db_steps

@router.get("/{recipe_id}", response_model=List[schemas.StepOut])
def get_step(recipe_id: int, db: Session = Depends(get_db)):
    db_steps = db.query(models.Step).filter(models.Step.recipe_id == recipe_id).all()
    if db_steps is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_steps
