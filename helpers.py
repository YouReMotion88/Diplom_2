import random
import string
import requests

from urls import BASE_URL, REGISTER, LOGIN, USER

# Генерируем случайную строку, чтобы пользователь был уникальным
def generate_random_string(length=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for _ in range(length))


def generate_user():
    return {
        "email": f"{generate_random_string()}@yandex.ru",
        "password": generate_random_string(),
        "name": generate_random_string()
    }


def create_user(user_data):
    return requests.post(
        BASE_URL + REGISTER,
        json=user_data
    )


def login_user(user_data):
    return requests.post(
        BASE_URL + LOGIN,
        json=user_data
    )


def delete_user(token):
    headers = {"Authorization": token}

    return requests.delete(
        BASE_URL + USER,
        headers=headers
    )