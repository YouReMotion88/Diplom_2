import pytest

from helpers import generate_user, create_user, delete_user, get_ingredients

@pytest.fixture
def registered_user():
    user = generate_user()

    response = create_user(user)

    token = None
    if response.status_code == 200:
        token = response.json()["accessToken"]

    yield user, response

    if token:
        delete_user(token)


@pytest.fixture
def ingredient():
    response = get_ingredients()

    ingredients = response.json()["data"]
    ingredient_id = ingredients[0]["_id"]

    return ingredient_id


@pytest.fixture
def ingredients():
    response = get_ingredients()

    ingredients = response.json()["data"]

    return [
        ingredients[0]["_id"],
        ingredients[1]["_id"]
    ]