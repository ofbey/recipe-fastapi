from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, schemas


router = APIRouter(
    prefix="/nutritions",
    tags=['Nutiritions']
)

@router.get("/", response_model=List[schemas.NutritionOut])
def get_nutritions(db: Session = Depends(get_db)):
    db_steps = db.query(models.Nutrition).all()
    return db_steps

@router.get("/{recipe_id}", response_model=List[schemas.NutritionOut])
def get_nutrition(recipe_id: int, db: Session = Depends(get_db)):
    db_steps = db.query(models.Nutrition).filter(models.Nutrition.recipe_id == recipe_id).all()
    if db_steps is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_steps
