import allure

from helpers import generate_user, create_user, delete_user

@allure.title("Создание уникального пользователя")
def test_create_unique_user():
    user = generate_user()

    with allure.step("Отправляем запрос на создание пользователя"):
        response = create_user(user)

    with allure.step("Получаем токен созданного пользователя для удаления после теста"):
        token = response.json()["accessToken"]

    with allure.step("Проверяем успешное создание пользователя"):
        assert response.status_code == 200
        assert response.json()["success"] is True

    with allure.step("Удаляем тестового пользователя"):
        delete_user(token)


@allure.title("Нельзя создать пользователя с уже существующим email")
def test_create_existing_user():
    user = generate_user()

    with allure.step("Создаём первого пользователя"):
        first_response = create_user(user)

    with allure.step("Получаем токен созданного пользователя для удаления после теста"):
        token = first_response.json()["accessToken"]

    with allure.step("Повторно отправляем запрос на создание пользователя с теми же данными"):
        response = create_user(user)

    with allure.step("Проверяем, что создание дубликата запрещено"):
        assert response.status_code == 403
        assert response.json()["success"] is False

    with allure.step("Удаляем тестового пользователя"):
        delete_user(token)


@allure.title("Нельзя создать пользователя без обязательного поля")
def test_create_user_without_name():
    user = generate_user()

    with allure.step("Удаляем обязательное поле name из данных пользователя"):
        del user["name"]

    with allure.step("Отправляем запрос на создание пользователя без обязательного поля"):
        response = create_user(user)

    with allure.step("Проверяем, что пользователь не был создан"):
        assert response.status_code == 403
        assert response.json()["success"] is False