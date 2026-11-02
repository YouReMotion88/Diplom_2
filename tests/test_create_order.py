import allure

from helpers import login_user, create_order


class TestCreateOrder:


    @allure.title("Создание заказа авторизованным пользователем")
    def test_create_order_with_authorization(self, registered_user, ingredient):
        user, _ = registered_user

        response_login = login_user(user)
        token = response_login.json()["accessToken"]

        response = create_order([ingredient], token)

        assert response.status_code == 200
        assert response.json()["success"] is True


    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_authorization(self, ingredient):

        response = create_order([ingredient])

        assert response.status_code == 200
        assert response.json()["success"] is True


    @allure.title("Создание заказа с несколькими ингредиентами")
    def test_create_order_with_multiple_ingredients(self, registered_user, ingredients):
        user, _ = registered_user

        response_login = login_user(user)
        token = response_login.json()["accessToken"]

        response = create_order(ingredients, token)

        assert response.status_code == 200
        assert response.json()["success"] is True


    @allure.title("Нельзя создать заказ без ингредиентов")
    def test_create_order_without_ingredients(self):

        response = create_order([])

        assert response.status_code == 400
        assert response.json()["success"] is False


    @allure.title("Создание заказа с невалидным хешем ингредиента")
    def test_create_order_with_invalid_ingredient_hash(self):

        response = create_order(["invalid_hash"])

        # По документации API ожидается HTTP 500,
        # фактически сервис возвращает HTTP 400.
        assert response.status_code == 500
        assert response.json()["success"] is False
        