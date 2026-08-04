import pytest

from helpers import generate_user, create_user, delete_user

@pytest.fixture
def registered_user():
    user = generate_user()

    response = create_user(user)

    token = response.json()["accessToken"]

    yield user

    delete_user(token)