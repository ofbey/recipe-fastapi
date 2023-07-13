from sqlalchemy.orm import Session
from app.models import Recipe, Ingredient
from app.database import SessionLocal

# Open a database session
db = SessionLocal()

# Define the recipe ID
recipe_id = 137739

# Retrieve the recipe by ID
recipe = db.query(Recipe).filter(Recipe.id == recipe_id).first()

# Retrieve the ingredients by recipe ID
ingredients = db.query(Ingredient).filter(Ingredient.recipe_id == recipe_id).all()

# Print the recipe information
print("Recipe:")
print("ID:", recipe.id)
print("Name:", recipe.name)
print("Minutes:", recipe.minutes)
print("Number of Steps:", recipe.n_steps)
print("Description:", recipe.description)
print("Number of Ingredients:", recipe.n_ingredients)

# Print the ingredient information
print("\nIngredients:")
for ingredient in ingredients:
    print("Ingredient:", ingredient.ingredient)
    print("----------------")

# Close the database session
db.close()
