from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, schemas


router = APIRouter(
    prefix="/ingredients",
    tags=['Ingredients']
)
@router.get("/", response_model=List[schemas.IngredientOut])
def get_ingredients(db: Session = Depends(get_db)):
    db_ingredients = db.query(models.Ingredient).all()
    return db_ingredients

@router.get("/{recipe_id}", response_model=schemas.IngredientOut)
def get_ingredient(recipe_id: int, db: Session = Depends(get_db)):
    db_ingredient = db.query(models.Ingredient).filter(models.Ingredient.recipe_id == recipe_id).first()
    if db_ingredient is None:
        raise HTTPException(status_code=404, detail="Ingredient not found")
    return db_ingredient
