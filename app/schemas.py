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
    name: str
    minutes: int
    n_steps: int
    description: str
    n_ingredients: int

    class Config:
        orm_mode = True

class RecipeIn(RecipeBase):
    pass

class RecipeOut(RecipeBase):
    id: int

    class Config:
        orm_mode = True