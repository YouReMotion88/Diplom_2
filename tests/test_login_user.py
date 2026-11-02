import allure

from helpers import login_user


class TestLoginUser:
    @allure.title("Успешный вход под существующим пользователем")
    def test_login_existing_user(self, registered_user):
        user, _ = registered_user
        response = login_user(user)

        assert response.status_code == 200
        assert response.json()["success"] is True


    @allure.title("Нельзя войти с неверным паролем")
    def test_login_with_invalid_password(self, registered_user):

        with allure.step("Подготавливаем данные пользователя с неверным паролем"):
            user, _ = registered_user
            user = user.copy()
            user["password"] = "wrong_password"
        
        response = login_user(user)

        assert response.status_code == 401
        assert response.json()["success"] is False