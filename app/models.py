from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


from .database import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    minutes = Column(Integer)
    n_steps = Column(Integer)
    description = Column(String)
    n_ingredients = Column(Integer)

class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer)
    ingredient = Column(String)
    ingredient_number = Column(Integer)



