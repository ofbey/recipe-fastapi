from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from .. import models, schemas, oauth2


router = APIRouter(
    prefix="/ingredients",
    tags=['Ingredients']
)
@router.get("/", response_model=List[schemas.IngredientOut])
def get_ingredients(
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
    db: Session = Depends(get_db)
    ):

    db_ingredients = db.query(models.Ingredient).filter(models.Ingredient.ingredient.contains(search)).limit(limit).offset(skip).all()
    return db_ingredients


@router.get("/{recipe_id}", response_model=List[schemas.IngredientOut])
def get_ingredient(
    recipe_id: int,
    db: Session = Depends(get_db)
    ):

    db_ingredients = db.query(models.Ingredient).filter(models.Ingredient.recipe_id == recipe_id).all()
    if not db_ingredients:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    return db_ingredients


@router.post("/{recipe_id}/ingredients", response_model=schemas.IngredientOut)
def create_ingredients(
    recipe_id: int,
    ingredients: List[schemas.IngredientIn],
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
    ):

    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if not db_recipe:
        raise HTTPException(status_code=404, detail="recipe not found")

    if db_recipe.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")


    for ingredient in ingredients:
        db_ingredient = models.Ingredient(
            recipe_id=recipe_id,
            ingredient=ingredient.ingredient,
            ingredient_number=ingredient.ingredient_number
        )
        db.add(db_ingredient)
        db.commit()
        db.refresh(db_ingredient)



    return db_ingredient

@router.put("/{ingredient_id}", response_model=schemas.IngredientOut)
def update_ingredient(
    ingredient_id: int,
    ingredient: schemas.IngredientIn,
    db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)
    ):

    db_ingredient = db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id).first()
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == db_ingredient.recipe_id).first()
    if db_recipe.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    db_ingredient.ingredient = ingredient.ingredient
    db_ingredient.ingredient_number = ingredient.ingredient_number

    db.commit()
    db.refresh(db_ingredient)

    return db_ingredient


@router.delete("/{ingredient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_ingredient(
    ingredient_id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user)
    ):

    db_ingredient = db.query(models.Ingredient).filter(models.Ingredient.id == ingredient_id).first()
    if not db_ingredient:
        raise HTTPException(status_code=404, detail="Ingredient not found")

    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == db_ingredient.recipe_id).first()
    if db_recipe.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")

    db.delete(db_ingredient)
    db.commit()

    return
