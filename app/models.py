from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Recipe(Base):
    __tablename__ = "recipes"
    id = Column(Integer, primary_key=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=True)
    name = Column(String)
    minutes = Column(Integer)
    n_steps = Column(Integer)
    description = Column(String)
    n_ingredients = Column(Integer)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'))
    ingredients = relationship("Ingredient", cascade="all, delete", backref="recipe")
    tags = relationship("Tag", cascade="all, delete", backref="recipe")
    steps = relationship("Step", cascade="all, delete", backref="recipe")
    nutrition = relationship("Nutrition", cascade="all, delete", backref="recipe")
    owner = relationship("User", backref="recipes")


class Ingredient(Base):
    __tablename__ = "ingredients"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    ingredient = Column(String)
    ingredient_number = Column(Integer)

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    tag = Column(String)
    tag_number = Column(Integer)

class Step(Base):
    __tablename__ = "steps"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    step = Column(String)
    step_number = Column(Integer)

class Nutrition(Base):
    __tablename__ = "nutritions"
    id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id"))
    calories = Column(Float)
    total_fat = Column(Float)
    sugar = Column(Float)
    sodium = Column(Float)
    protein = Column(Float)
    saturated_fat = Column(Float)
    carbohydrates = Column(Float)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text('now()'))

class Like(Base):
    __tablename__ = "likes"
    user_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), primary_key=True)
    recipe_id = Column(Integer, ForeignKey(
        "recipes.id", ondelete="CASCADE"), primary_key=True)