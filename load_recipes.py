from sqlalchemy.orm import Session
from app.models import Recipe, Ingredient, Tag, Step, Nutrition
from app.database import SessionLocal
import pandas as pd
import time

db = SessionLocal()

def load_recipes(csv_file, owner_id):
    recipe_df = pd.read_csv(csv_file)
    recipe_df = recipe_df.head(5)

    recipe_data = recipe_df.to_dict(orient='records')

    for row in recipe_data:
        recipe_id = row['id']

        if pd.isnull(recipe_id):
            continue

        recipe = Recipe(
            id=recipe_id,
            name=row['name'],
            minutes=int(row['minutes']),
            n_steps=int(row['n_steps']),
            description=row['description'],
            n_ingredients=int(row['n_ingredients']),
            owner_id=owner_id

        )

        db.add(recipe)

    db.commit()


def load_ingredients(csv_file):
    ingredient_df = pd.read_csv(csv_file)
    ingredient_df = ingredient_df.head(5)
    ingredient_data = ingredient_df.to_dict(orient='records')

    for row in ingredient_data:
        ingredient_id = int(row['id'])

        # Check if the recipe_id exists in the Recipe table
        db_recipe = db.query(Recipe).filter(Recipe.id == ingredient_id).first()
        if db_recipe is None:
            continue

        ingredient = Ingredient(
            recipe_id=ingredient_id,
            ingredient=row['ingredients'],
            ingredient_number=int(row['ingredient_number'])
        )

        db.add(ingredient)

    db.commit()


def load_tags(csv_file):
    tags_df = pd.read_csv(csv_file)
    tags_df = tags_df.head(5)
    tags_data = tags_df.to_dict(orient='records')

    for row in tags_data:
        tags_id = int(row['id'])

        db_recipe = db.query(Recipe).filter(Recipe.id == tags_id).first()
        if db_recipe is None:
            continue


        tag = Tag(
            recipe_id=tags_id,
            tag=row['tags'],
            tag_number=int(row['tag_number'])
        )

        db.add(tag)

    db.commit()


def load_steps(csv_file):
    steps_df = pd.read_csv(csv_file)
    steps_df = steps_df.head(5)
    steps_data = steps_df.to_dict(orient='records')

    for row in steps_data:
        steps_id = int(row['id'])

        db_recipe = db.query(Recipe).filter(Recipe.id == steps_id).first()
        if db_recipe is None:
            continue

        step = Step(
            recipe_id=steps_id,
            step=row['steps'],
            step_number=int(row['step_number'])
        )

        db.add(step)

    db.commit()


def load_nutrition(csv_file):
    nutrition_df = pd.read_csv(csv_file)
    nutrition_df = nutrition_df.head(5)

    nutrition_data = nutrition_df.to_dict(orient='records')

    for row in nutrition_data:
        nutrition_id = int(row['id']) if not pd.isnull(row['id']) else None

        # Check if the recipe_id exists in the Recipe table
        db_recipe = db.query(Recipe).filter(Recipe.id == nutrition_id).first()
        if db_recipe is None:
            continue

        nutrition = Nutrition(
            recipe_id=nutrition_id,
            calories=row['calories'],
            total_fat=row['total_fat'],
            sugar=row['sugar'],
            sodium=row['sodium'],
            protein=row['protein'],
            saturated_fat=row['saturated_fat'],
            carbohydrates=row['carbohydrates']
        )

        db.add(nutrition)

    db.commit()


recipe_csv_file = 'data/recipes_table.csv'
ingredient_csv_file = 'data/ingredients_table.csv'
tags_csv_file = 'data/tags_table.csv'
steps_csv_file = 'data/steps_table.csv'
nutrition_csv_file = 'data/nutrition_table.csv'

start_time = time.time()

owner_id = 1
load_recipes(recipe_csv_file, owner_id)
load_ingredients(ingredient_csv_file)
load_tags(tags_csv_file)
load_steps(steps_csv_file)
load_nutrition(nutrition_csv_file)

end_time = time.time()
execution_time = end_time - start_time

print(f"Loading data took {execution_time} seconds")

db.close()
