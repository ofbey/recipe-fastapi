import pandas as pd
import ast

#parse stringified lists
def parse_str_list(s):
    return ast.literal_eval(s)

df = pd.read_csv('recipes.csv')

df_clean = df.drop(columns=['contributor_id', 'submitted'])

df_clean = df_clean.dropna()

# Parse the stringified lists in the 'tags', 'nutrition', 'steps', 'ingredients' columns
df_clean['tags'] = df_clean['tags'].apply(parse_str_list)
df_clean['nutrition'] = df_clean['nutrition'].apply(parse_str_list)
df_clean['steps'] = df_clean['steps'].apply(parse_str_list)
df_clean['ingredients'] = df_clean['ingredients'].apply(parse_str_list)


tags_table = df_clean.explode('tags')[['id', 'tags']]
steps_table = df_clean.explode('steps')[['id', 'steps']]
ingredients_table = df_clean.explode('ingredients')[['id', 'ingredients']]

nutrition_df = pd.DataFrame(df_clean['nutrition'].to_list(), columns=['calories', 'total_fat', 'sugar', 'sodium', 'protein', 'saturated_fat', 'carbohydrates'])
nutrition_df['id'] = df_clean['id']
nutrition_df = nutrition_df.dropna(subset=['id'])
nutrition_table = nutrition_df[['id', 'calories', 'total_fat', 'sugar', 'sodium', 'protein', 'saturated_fat', 'carbohydrates']]

tags_table['tag_number'] = tags_table.groupby('id').cumcount() + 1
steps_table['step_number'] = steps_table.groupby('id').cumcount() + 1
ingredients_table['ingredient_number'] = ingredients_table.groupby('id').cumcount() + 1

df_clean = df_clean.drop(columns=['tags', 'steps', 'ingredients', 'nutrition'])

df_clean.to_csv('recipes_table.csv', index=False)
tags_table.to_csv('tags_table.csv', index=False)
steps_table.to_csv('steps_table.csv', index=False)
ingredients_table.to_csv('ingredients_table.csv', index=False)
nutrition_table.to_csv('nutrition_table.csv', index=False)
