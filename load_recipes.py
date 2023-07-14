from sqlalchemy.orm import Session
from app.models import Recipe, Ingredient, Tags, Steps, Nutrition
from app.database import SessionLocal
import pandas as pd


db = SessionLocal()


def load_recipes(csv_file):
    recipe_df = pd.read_csv(csv_file)
    recipe_df = recipe_df.head(10)

    for _, row in recipe_df.iterrows():
        recipe = Recipe(
            id=int(row['id']),
            name=row['name'],
            minutes=int(row['minutes']),
            n_steps=int(row['n_steps']),
            description=row['description'],
            n_ingredients=int(row['n_ingredients'])
        )

        db.add(recipe)

    db.commit()


def load_ingredients(csv_file):
    ingredient_df = pd.read_csv(csv_file)
    ingredient_df = ingredient_df.head(10)

    for _, row in ingredient_df.iterrows():
        ingredient = Ingredient(
            recipe_id=int(row['id']),
            ingredient=row['ingredients'],
            ingredient_number=int(row['ingredient_number'])
        )

        db.add(ingredient)

    db.commit()


def load_tags(csv_file):
    tags_df = pd.read_csv(csv_file)
    tags_df = tags_df.head(10)

    for _, row in tags_df.iterrows():
        tag = Tags(
            recipe_id=int(row['id']),
            tag=row['tags'],
            tag_number=int(row['tag_number'])
        )

        db.add(tag)

    db.commit()


def load_steps(csv_file):
    steps_df = pd.read_csv(csv_file)
    steps_df = steps_df.head(10)

    for _, row in steps_df.iterrows():
        step = Steps(
            recipe_id=int(row['id']),
            step=row['steps'],
            step_number=int(row['step_number'])
        )

        db.add(step)

    db.commit()


from app.models import Nutrition

def load_nutrition(csv_file):
    nutrition_df = pd.read_csv(csv_file)
    nutrition_df = nutrition_df.head(10)

    for _, row in nutrition_df.iterrows():

        nutrition_id = int(row['id']) if not pd.isnull(row['id']) else None


        if db.query(Recipe).filter(Recipe.id == nutrition_id).first() is None:
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




recipe_csv_file = 'recipe_dataset/recipes_table.csv'
ingredient_csv_file = 'recipe_dataset/ingredients_table.csv'
tags_csv_file = 'recipe_dataset/tags_table.csv'
steps_csv_file = 'recipe_dataset/steps_table.csv'
nutrition_csv_file = 'recipe_dataset/nutrition_table.csv'

load_recipes(recipe_csv_file)
load_ingredients(ingredient_csv_file)
load_tags(tags_csv_file)
load_steps(steps_csv_file)
load_nutrition(nutrition_csv_file)


db.close()
