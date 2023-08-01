from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app import schemas
from app.main import app
from app.config import settings
from app.database import get_db
from app.database import Base
from jose import jwt
from app.oauth2 import create_access_token
from app import models

#############
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

@pytest.fixture
def test_user(client):
    user_data = {"email": "fth@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "fth123@gmail.com",
                 "password": "password123"}
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user


@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client

@pytest.fixture
def test_recipes(test_user, session, test_user2):
    recipes_data = [{
            "name": "First Recipe",
            "minutes": 30,
            "n_steps": 5,
            "description": "This is the first recipe",
            "n_ingredients": 10,
            "owner_id": test_user['id']
        }, {
            "name": "Second Recipe",
            "minutes": 45,
            "n_steps": 8,
            "description": "This is the second recipe",
            "n_ingredients": 12,
            "owner_id": test_user['id']
        },
            {
            "name": "Third Recipe",
            "minutes": 60,
            "n_steps": 10,
            "description": "This is the third recipe",
            "n_ingredients": 15,
            "owner_id": test_user['id']
        }, {
            "name": "Fourth Recipe",
            "minutes": 20,
            "n_steps": 3,
            "description": "This is the fourth recipe",
            "n_ingredients": 5,
            "owner_id": test_user2['id']
        }]


    def create_recipe_model(recipe):
        return models.Recipe(**recipe)

    recipe_map = map(create_recipe_model, recipes_data)
    recipe = list(recipe_map)

    session.add_all(recipe)
    session.commit()

    recipe = session.query(models.Recipe).all()
    return recipe