from typing import List
from pydantic import BaseModel



class RecipeBase(BaseModel):
    name: str
    minutes: int
    n_steps: int
    description: str
    n_ingredients: int

class RecipeList(RecipeBase):
    id: int

    class Config:
        orm_mode = True


class RecipeIn(RecipeBase):
    pass

class RecipeOut(RecipeBase):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel

class IngredientBase(BaseModel):
    ingredient: str
    ingredient_number: int

class IngredientCreate(IngredientBase):
    pass

class IngredientOut(IngredientBase):
    id: int
    recipe_id: int

    class Config:
        orm_mode = True

class TagBase(BaseModel):
    tag: str
    tag_number: int

class TagCreate(TagBase):
    pass

class TagOut(TagBase):
    id: int
    recipe_id: int

    class Config:
        orm_mode = True

class StepBase(BaseModel):
    step: str
    step_number: int

class StepCreate(StepBase):
    pass

class StepOut(StepBase):
    id: int
    recipe_id: int

    class Config:
        orm_mode = True

class NutritionBase(BaseModel):
    calories: float
    total_fat: float
    sugar: float
    sodium: float
    protein: float
    saturated_fat: float
    carbohydrates: float

class NutritionCreate(NutritionBase):
    pass

class NutritionOut(NutritionBase):
    id: int
    recipe_id: int

    class Config:
        orm_mode = True
