from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class RecipeBase(BaseModel):
    name: str
    minutes: int
    n_steps: int
    description: str
    n_ingredients: int

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

class IngredientIn(IngredientBase):
    pass

class IngredientOut(IngredientBase):
    id: int
    recipe_id: int

    class Config:
        orm_mode = True

class TagBase(BaseModel):
    tag: str
    tag_number: int

class TagIn(TagBase):
    pass

class TagOut(TagBase):
    id: int
    recipe_id: int

    class Config:
        orm_mode = True

class StepBase(BaseModel):
    step: str
    step_number: int

class StepIn(StepBase):
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

class NutritionIn(NutritionBase):
    pass

class NutritionOut(NutritionBase):
    id: int
    recipe_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserIn(UserBase):
    pass

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None