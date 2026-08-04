import allure

from helpers import login_user, create_order


@allure.title("Создание заказа авторизованным пользователем")
def test_create_order_with_authorization(registered_user, ingredient):

    with allure.step("Авторизуем пользователя и получаем токен"):
        response_login = login_user(registered_user)
        token = response_login.json()["accessToken"]

    with allure.step("Создаём заказ с ингредиентом"):
        response = create_order([ingredient], token)

    with allure.step("Проверяем успешное создание заказа"):
        assert response.status_code == 200
        assert response.json()["success"] is True

@allure.title("Создание заказа без авторизации")
def test_create_order_without_authorization(ingredient):

    with allure.step("Создаём заказ без авторизации"):
        response = create_order([ingredient])

    with allure.step("Проверяем успешное создание заказа"):
        assert response.status_code == 200
        assert response.json()["success"] is True


@allure.title("Создание заказа с несколькими ингредиентами")
def test_create_order_with_multiple_ingredients(registered_user, ingredients):

    with allure.step("Авторизуем пользователя и получаем токен"):
        response_login = login_user(registered_user)
        token = response_login.json()["accessToken"]

    with allure.step("Создаём заказ с несколькими ингредиентами"):
        response = create_order(ingredients, token)

    with allure.step("Проверяем успешное создание заказа"):
        assert response.status_code == 200
        assert response.json()["success"] is True

@allure.title("Нельзя создать заказ без ингредиентов")
def test_create_order_without_ingredients():

    with allure.step("Создаём заказ без ингредиентов"):
        response = create_order([])

    with allure.step("Проверяем, что заказ не был создан"):
        assert response.status_code == 400
        assert response.json()["success"] is False


@allure.title("Создание заказа с невалидным хешем ингредиента")
def test_create_order_with_invalid_ingredient_hash():

    with allure.step("Создаём заказ с невалидным хешем ингредиента"):
        response = create_order(["invalid_hash"])

    with allure.step("Проверяем ошибку создания заказа"):
        # По документации API ожидается HTTP 500,
        # фактически сервис возвращает HTTP 400.
        assert response.status_code == 500
        assert response.json()["success"] is False
        