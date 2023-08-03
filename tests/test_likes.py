import pytest
from app import models


@pytest.fixture()
def test_likes(test_recipes, session, test_user):
    new_like = models.Like(recipe_id=test_recipes[3].id, user_id=test_user['id'])
    session.add(new_like)
    session.commit()

def test_like_on_recipe(authorized_client, test_recipes):
    res = authorized_client.post(
        "/like/", json={"recipe_id": test_recipes[3].id, "dir": 1})
    assert res.status_code == 201


def test_like_twice_recipe(authorized_client, test_recipes, test_likes):
    res = authorized_client.post(
        "/like/", json={"recipe_id": test_recipes[3].id, "dir": 1})
    assert res.status_code == 409


def test_delete_like(authorized_client, test_recipes, test_likes):
    res = authorized_client.post(
        "/like/", json={"recipe_id": test_recipes[3].id, "dir": 0})
    assert res.status_code == 201


def test_delete_like_non_exist(authorized_client, test_recipes):
    res = authorized_client.post(
        "/like/", json={"recipe_id": test_recipes[3].id, "dir": 0})
    assert res.status_code == 404


def test_like_recipe_non_exist(authorized_client, test_recipes):
    res = authorized_client.post(
        "/like/", json={"recipe_id": 10000000, "dir": 1})
    assert res.status_code == 404


def test_recipe_unauthorized_user(client, test_recipes):
    res = client.post(
        "/like/", json={"post_id": test_recipes[3].id, "dir": 1})
    assert res.status_code == 401