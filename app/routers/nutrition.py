from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, schemas, oauth2


router = APIRouter(
    prefix="/nutritions",
    tags=['Nutiritions']
)

@router.get("/", response_model=List[schemas.NutritionOut])
def get_nutritions(
    limit: int = 10,
    skip: int = 0,
    db: Session = Depends(get_db)):
    db_steps = db.query(models.Nutrition).limit(limit).offset(skip).all()
    return db_steps

@router.get("/{recipe_id}", response_model=List[schemas.NutritionOut])
def get_nutrition(recipe_id: int, db: Session = Depends(get_db)):
    db_steps = db.query(models.Nutrition).filter(models.Nutrition.recipe_id == recipe_id).all()
    if db_steps is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_steps

@router.post("/{recipe_id}/nutritions", response_model=schemas.NutritionOut)
def create_nutrition(
    recipe_id: int,
    nutrition: schemas.NutritionIn,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")

    if db_recipe.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    db_nutrition = models.Nutrition(
        recipe_id=recipe_id,
        calories=nutrition.calories,
        total_fat=nutrition.total_fat,
        sugar=nutrition.sugar,
        sodium=nutrition.sodium,
        protein=nutrition.protein,
        saturated_fat=nutrition.saturated_fat,
        carbohydrates=nutrition.carbohydrates,
    )
    db.add(db_nutrition)
    db.commit()
    db.refresh(db_nutrition)

    return db_nutrition

@router.put("/{nutrition_id}", response_model=schemas.NutritionOut)
def update_nutrition(
    nutrition_id: int,
    nutrition: schemas.NutritionIn,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    db_nutrition = db.query(models.Nutrition).filter(models.Nutrition.id == nutrition_id).first()

    if not db_nutrition:
        raise HTTPException(status_code=404, detail="Nutrition not found")

    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == db_nutrition.recipe_id).first()

    if db_recipe.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    db_nutrition.calories = nutrition.calories
    db_nutrition.total_fat = nutrition.total_fat
    db_nutrition.sugar = nutrition.sugar
    db_nutrition.sodium = nutrition.sodium
    db_nutrition.protein = nutrition.protein
    db_nutrition.saturated_fat = nutrition.saturated_fat
    db_nutrition.carbohydrates = nutrition.carbohydrates

    db.commit()
    db.refresh(db_nutrition)

    return db_nutrition

@router.delete("/{nutrition_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_nutrition(
    nutrition_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
):
    db_nutrition = db.query(models.Nutrition).filter(models.Nutrition.id == nutrition_id).first()

    if not db_nutrition:
        raise HTTPException(status_code=404, detail="Nutrition not found")

    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == db_nutrition.recipe_id).first()

    if db_recipe.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    db.delete(db_nutrition)
    db.commit()

    return