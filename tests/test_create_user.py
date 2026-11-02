import allure

from helpers import generate_user, create_user


class TestCreateUser:


    @allure.title("Создание уникального пользователя")
    def test_create_unique_user(self, registered_user):
        _, response = registered_user

        assert response.status_code == 200
        assert response.json()["success"] is True


    @allure.title("Нельзя создать пользователя с уже существующим email")
    def test_create_existing_user(self, registered_user):
        user, _ = registered_user

        response = create_user(user)

        assert response.status_code == 403
        assert response.json()["success"] is False


    @allure.title("Нельзя создать пользователя без обязательного поля")
    def test_create_user_without_name(self):
        user = generate_user()

        with allure.step("Удаляем обязательное поле name"):
            del user["name"]
       
        response = create_user(user)

        assert response.status_code == 403
        assert response.json()["success"] is False