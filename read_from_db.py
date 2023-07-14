from sqlalchemy.orm import Session
from app.models import Recipe, Ingredient, Tag, Step, Nutrition
from app.database import SessionLocal


db = SessionLocal()

recipe_id = 137739
recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()
ingredients = db.query(Ingredient).filter(Ingredient.recipe_id == recipe_id).all()
tags = db.query(Tag).filter(Tag.recipe_id == recipe_id).all()
steps = db.query(Step).filter(Step.recipe_id == recipe_id).all()
nutrition = db.query(Nutrition).filter(Nutrition.recipe_id == recipe_id).first()


print("Recipe:")
print("ID:", recipe.id)
print("Name:", recipe.name)
print("Minutes:", recipe.minutes)
print("Number of Steps:", recipe.n_steps)
print("Description:", recipe.description)
print("Number of Ingredients:", recipe.n_ingredients)


print("\nIngredients:")
for ingredient in ingredients:
    print("Ingredient:", ingredient.ingredient)
    print("----------------")


print("\nTags:")
for tag in tags:
    print("Tag:", tag.tag)
    print("----------------")


print("\nSteps:")
for step in steps:
    print("Step:", step.step)
    print("----------------")

print("\nNutrition:")
print("Calories:", nutrition.calories)
print("Total Fat:", nutrition.total_fat)
print("Sugar:", nutrition.sugar)
print("Sodium:", nutrition.sodium)
print("Protein:", nutrition.protein)
print("Saturated Fat:", nutrition.saturated_fat)
print("Carbohydrates:", nutrition.carbohydrates)


db.close()
