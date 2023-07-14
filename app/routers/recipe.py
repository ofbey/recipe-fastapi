from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..models import Recipe
from app.schemas import RecipeIn, RecipeOut
from typing import List, Optional
from ..database import get_db
from .. import models, schemas


router = APIRouter(
    prefix="/recipes",
    tags=['Recipes']
)

@router.get("/", response_model=List[schemas.RecipeOut])
def get_recipes(page: int = 0, page_size: int = 10, db: Session = Depends(get_db)):
    db_recipes = db.query(models.Recipe).offset(page * page_size).limit(page_size).all()
    return db_recipes

# @router.get("/", response_model=List[schemas.RecipeOut])
# def get_recipes(db: Session = Depends(get_db)):
#     db_recipes = db.query(models.Recipe).all()
#     print(db_recipes)
#     return db_recipes

@router.get("/{recipe_id}", response_model=RecipeOut)
def get_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return db_recipe

@router.get("/search/{recipe_name}", response_model=List[schemas.RecipeOut])
def search_recipes(recipe_name: str, db: Session = Depends(get_db)):
    recipes = db.query(models.Recipe).filter(models.Recipe.name.contains(recipe_name)).all()
    return recipes

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=RecipeOut)
def create_recipe(recipe: RecipeIn, db: Session = Depends(get_db)):
    db_recipe = Recipe(**recipe.dict())
    db.add(db_recipe)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@router.put("/{recipe_id}", response_model=RecipeOut)
def update_recipe(recipe_id: int, recipe: RecipeIn, db: Session = Depends(get_db)):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    update_data = recipe.dict(exclude_unset=True)
    db.query(Recipe).filter(Recipe.id == recipe_id).update(update_data)
    db.commit()
    db.refresh(db_recipe)
    return db_recipe

@router.delete("/{recipe_id}", response_model=RecipeOut)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")
    db.delete(db_recipe)
    db.commit()
    return db_recipe



# @router.post("/", status_code=status.HTTP_201_CREATED, response_model=RecipeOut)
# def create_recipe(recipe: RecipeIn):
#     with get_db() as session:
#         db_recipe = Recipe(**recipe.dict(exclude={"tags", "steps", "ingredients", "nutrition"}))
#         session.add(db_recipe)

#         for tag in recipe.tags:
#             db_tag = Tag(**tag.dict(), recipe=db_recipe)
#             session.add(db_tag)

#         for step in recipe.steps:
#             db_step = Step(**step.dict(), recipe=db_recipe)
#             session.add(db_step)

#         for ingredient in recipe.ingredients:
#             db_ingredient = Ingredient(**ingredient.dict(), recipe=db_recipe)
#             session.add(db_ingredient)

#         db_nutrition = Nutrition(**recipe.nutrition.dict(), recipe=db_recipe)
#         session.add(db_nutrition)

#         session.commit()
#         session.refresh(db_recipe)
#         return db_recipe



# @router.put("/{recipe_id}", response_model=RecipeOut)
# def update_recipe(recipe_id: int, recipe: RecipeIn):
#     with get_db() as session:
#         db_recipe = session.query(Recipe).get(recipe_id)
#         if db_recipe is None:
#             raise HTTPException(status_code=404, detail="Recipe not found")

#         for key, value in recipe.dict(exclude={"tags", "steps", "ingredients", "nutrition"}).items():
#             setattr(db_recipe, key, value)

#         if recipe.tags is not None:
#             db_recipe.tags = []
#             for tag in recipe.tags:
#                 db_tag = Tag(**tag.dict(), recipe=db_recipe)
#                 session.add(db_tag)

#         if recipe.steps is not None:
#             db_recipe.steps = []
#             for step in recipe.steps:
#                 db_step = Step(**step.dict(), recipe=db_recipe)
#                 session.add(db_step)

#         if recipe.ingredients is not None:
#             db_recipe.ingredients = []
#             for ingredient in recipe.ingredients:
#                 db_ingredient = Ingredient(**ingredient.dict(), recipe=db_recipe)
#                 session.add(db_ingredient)

#         if recipe.nutrition is not None:
#             db_recipe.nutrition = Nutrition(**recipe.nutrition.dict(), recipe=db_recipe)
#             session.add(db_recipe.nutrition)

#         session.commit()
#         return db_recipe

##############################

