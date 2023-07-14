import pandas as pd

# Read the recipes file
recipes_df = pd.read_csv('recipes.csv')
recipes_head = recipes_df.head(5)
print(recipes_head)
print()


# Read the cleaned recipes file
recipes_df = pd.read_csv('data/recipes_table.csv')
recipes_head = recipes_df.head(20)
print("Recipes:")
print(recipes_head)
print()

# Read the ingredients table
ingredients_df = pd.read_csv('data/ingredients_table.csv')
ingredients_head = ingredients_df.head(5)
print("Ingredients:")
print(ingredients_head)
print()


# Read the tags table
tags_df = pd.read_csv('data/tags_table.csv')
tags_head = tags_df.head(5)
print("Tags:")
print(tags_head)
print()

# Read the steps table
steps_df = pd.read_csv('data/steps_table.csv')
steps_head = steps_df.head(5)
print("Steps:")
print(steps_head)
print()


# Read the nutrition table
nutrition_df = pd.read_csv('data/nutrition_table.csv')
nutrition_head = nutrition_df.head(5)
print("Nutrition:")
print(nutrition_head)

recipes_df = pd.read_csv('data/recipes_table.csv')
recipes_has_nan = recipes_df['id'].isnull().any()
print("Recipes table has NaN values in the 'id' column:", recipes_has_nan)

# Read the tags table
tags_df = pd.read_csv('data/tags_table.csv')
tags_has_nan = tags_df['id'].isnull().any()
print("Tags table has NaN values in the 'id' column:", tags_has_nan)

# Read the steps table
steps_df = pd.read_csv('data/steps_table.csv')
steps_has_nan = steps_df['id'].isnull().any()
print("Steps table has NaN values in the 'id' column:", steps_has_nan)

# Read the ingredients table
ingredients_df = pd.read_csv('data/ingredients_table.csv')
ingredients_has_nan = ingredients_df['id'].isnull().any()
print("Ingredients table has NaN values in the 'id' column:", ingredients_has_nan)

# Read the nutrition table
nutrition_df = pd.read_csv('data/nutrition_table.csv')
nutrition_has_nan = nutrition_df['id'].isnull().any()
print("Nutrition table has NaN values in the 'id' column:", nutrition_has_nan)


