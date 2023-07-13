from sqlalchemy.orm import Session
from app.models import Recipe, Ingredient
from app.database import SessionLocal

import pandas as pd

# Open a database session
db = SessionLocal()

# Read the CSV file for recipes
recipe_csv_file = 'recipe_dataset/recipes_table.csv'
recipe_df = pd.read_csv(recipe_csv_file)
recipe_df = recipe_df.head(10)

# Iterate over the recipe DataFrame rows
for _, row in recipe_df.iterrows():
    # Create a new Recipe object and populate its attributes from the DataFrame row
    recipe = Recipe(
        id=int(row['id']),
        name=row['name'],
        minutes=int(row['minutes']),
        n_steps=int(row['n_steps']),
        description=row['description'],
        n_ingredients=int(row['n_ingredients'])
    )

    # Add the Recipe object to the session
    db.add(recipe)

# Commit the changes to the database
db.commit()

# Read the CSV file for ingredients
ingredient_csv_file = 'recipe_dataset/ingredients_table.csv'
ingredient_df = pd.read_csv(ingredient_csv_file)
ingredient_df = ingredient_df.head(10)

# Iterate over the ingredient DataFrame rows
for _, row in ingredient_df.iterrows():
    # Create a new Ingredient object and populate its attributes from the DataFrame row
    ingredient = Ingredient(
        recipe_id=int(row['id']),
        ingredient=row['ingredients'],
        ingredient_number=int(row['ingredient_number'])
    )

    # Add the Ingredient object to the session
    db.add(ingredient)

# Commit the changes to the database
db.commit()

# Close the database session
db.close()
