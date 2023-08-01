import pytest
from app import schemas

def test_get_all_recipes(authorized_client, test_recipes):
    res = authorized_client.get("/recipes/")

    def validate(recipe):
        return schemas.RecipeOut(**recipe)
    recipes_map = map(validate, res.json())
    recipes_list = list(recipes_map)

    assert len(res.json()) == len(test_recipes)
    assert res.status_code == 200

def test_get_one_recipe_not_exist(authorized_client):
    res = authorized_client.get(f"/recipes/88888")
    assert res.status_code == 404

def test_get_one_recipe(authorized_client, test_recipes):
    res = authorized_client.get(f"/recipes/{test_recipes[0].id}")
    recipe = schemas.RecipeOut(**res.json())
    assert recipe.id == test_recipes[0].id
    assert recipe.name == test_recipes[0].name
    assert recipe.minutes == test_recipes[0].minutes
    assert recipe.n_steps == test_recipes[0].n_steps
    assert recipe.description == test_recipes[0].description
    assert recipe.n_ingredients == test_recipes[0].n_ingredients
    assert recipe.owner_id == test_recipes[0].owner_id

@pytest.mark.parametrize("name, minutes, n_steps, description, n_ingredients", [
    ("New Recipe", 45, 10, "This is a new recipe", 12),
    ("Pizza", 30, 7, "Delicious homemade pizza", 9),
    ("Burger", 20, 5, "Tasty burger recipe", 8),
])
def test_create_recipe(authorized_client, test_user, name, minutes, n_steps, description, n_ingredients):
    res = authorized_client.post(
        "/recipes/", json={"name": name, "minutes": minutes, "n_steps": n_steps, "description": description, "n_ingredients": n_ingredients})

    created_recipe = schemas.RecipeOut(**res.json())
    assert res.status_code == 201
    assert created_recipe.name == name
    assert created_recipe.minutes == minutes
    assert created_recipe.n_steps == n_steps
    assert created_recipe.description == description
    assert created_recipe.n_ingredients == n_ingredients
    assert created_recipe.owner_id == test_user['id']

def test_create_recipe_without_owner_id(authorized_client, test_user):
    res = authorized_client.post(
        "/recipes/", json={"name": "New Recipe", "minutes": 30, "n_steps": 5, "description": "This is a new recipe", "n_ingredients": 10})

    created_recipe = schemas.RecipeOut(**res.json())
    assert res.status_code == 201
    assert created_recipe.owner_id == test_user['id']

def test_unauthorized_user_create_recipe(client ):
    res = client.post(
        "/recipes/", json={"name": "New Recipe", "minutes": 30, "n_steps": 5, "description": "This is a new recipe", "n_ingredients": 10})
    assert res.status_code == 401

def test_unauthorized_user_delete_recipe(client, test_recipes):
    res = client.delete(
        f"/recipes/{test_recipes[0].id}")
    assert res.status_code == 401

def test_delete_recipe_success(authorized_client,  test_recipes):
    res = authorized_client.delete(
        f"/recipes/{test_recipes[0].id}")

    assert res.status_code == 204

def test_delete_recipe_non_exist(authorized_client, ):
    res = authorized_client.delete(
        f"/recipes/8000000")

    assert res.status_code == 404

def test_delete_other_user_recipe(authorized_client, test_recipes):
    res = authorized_client.delete(
        f"/recipes/{test_recipes[3].id}")
    assert res.status_code == 403

def test_update_recipe(authorized_client, test_recipes):
    data = {
        "name": "Updated Recipe",
        "minutes": 50,
        "n_steps": 8,
        "description": "Updated recipe description",
        "n_ingredients": 15,
        "id": test_recipes[0].id
    }
    res = authorized_client.put(f"/recipes/{test_recipes[0].id}", json=data)
    updated_recipe = schemas.RecipeOut(**res.json())
    assert res.status_code == 200
    assert updated_recipe.name == data['name']
    assert updated_recipe.minutes == data['minutes']
    assert updated_recipe.n_steps == data['n_steps']
    assert updated_recipe.description == data['description']
    assert updated_recipe.n_ingredients == data['n_ingredients']

def test_update_other_user_recipe(authorized_client, test_recipes):
    data = {
        "name": "Updated Recipe",
        "minutes": 50,
        "n_steps": 8,
        "description": "Updated recipe description",
        "n_ingredients": 15,
        "id": test_recipes[3].id
    }
    res = authorized_client.put(f"/recipes/{test_recipes[3].id}", json=data)
    assert res.status_code == 403

def test_unauthorized_user_update_recipe(client, test_recipes):
    res = client.put(
        f"/recipes/{test_recipes[0].id}")
    assert res.status_code == 401

def test_update_recipe_non_exist(authorized_client, test_recipes):
    data = {
        "name": "Updated Recipe",
        "minutes": 50,
        "n_steps": 8,
        "description": "Updated recipe description",
        "n_ingredients": 15,
        "id": test_recipes[3].id
    }
    res = authorized_client.put(
        f"/recipes/8000000", json=data)

    assert res.status_code == 404
