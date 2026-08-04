import allure

from helpers import login_user


@allure.title("Успешный вход под существующим пользователем")
def test_login_existing_user(registered_user):

    with allure.step("Отправляем данные пользователя для авторизации"):
        response = login_user(registered_user)

    with allure.step("Проверяем успешную авторизацию"):
        assert response.status_code == 200
        assert response.json()["success"] is True


@allure.title("Нельзя войти с неверным паролем")
def test_login_with_invalid_password(registered_user):

    with allure.step("Подготавливаем данные пользователя с неверным паролем"):
    # Создаём копию словаря, чтобы не изменять объект
        user = registered_user.copy()
        user["password"] = "wrong_password"

    with allure.step("Отправляем запрос на авторизацию с неверным паролем"):
        response = login_user(user)

    with allure.step("Проверяем, что авторизация не выполнена"):
        assert response.status_code == 401
        assert response.json()["success"] is False