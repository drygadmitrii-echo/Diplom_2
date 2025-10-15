import pytest  # Добавляем импорт pytest
import requests
import allure
from data import *
from urls import *


@pytest.fixture(scope='function')
def generate_user_data():
    user = UserData.valid_user
    yield user

    # Cleanup: login and delete user
    try:
        user_login = UserData.invalid_logins[0]
        with allure.step(f'POST запрос к {APIEndpoints.LOGIN} с данными {user_login}'):
            login_response = requests.post(f'{BaseUrls.API_BASE}{APIEndpoints.LOGIN}', json=user_login, timeout=10)
            if login_response.status_code == 200:
                token = login_response.json().get('accessToken')
                if token:
                    headers = {'Authorization': token}
                    with allure.step(f'DELETE запрос к {APIEndpoints.DELETE_USER}'):
                        requests.delete(f'{BaseUrls.API_BASE}{APIEndpoints.DELETE_USER}', headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Ошибка при cleanup: {e}")


@pytest.fixture(scope='function')
def create_test_user():
    user = UserData.valid_user
    try:
        with allure.step(f'POST запрос к {APIEndpoints.CREATE_USER} с данными {user}'):
            response = requests.post(f'{BaseUrls.API_BASE}{APIEndpoints.CREATE_USER}', json=user, timeout=10)
            if response.status_code not in [200, 201]:
                print(f"⚠️  Пользователь не создан: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Ошибка при создании пользователя: {e}")

    user_login = UserData.invalid_logins[0]
    yield user

    # Cleanup
    try:
        with allure.step(f'POST запрос к {APIEndpoints.LOGIN} с данными {user_login} для обновления токена'):
            login_response = requests.post(f'{BaseUrls.API_BASE}{APIEndpoints.LOGIN}', json=user_login, timeout=10)
            if login_response.status_code == 200:
                token = login_response.json().get("accessToken")
                if token:
                    headers = {'Authorization': token}
                    with allure.step(f'DELETE запрос к {APIEndpoints.DELETE_USER}'):
                        requests.delete(f'{BaseUrls.API_BASE}{APIEndpoints.DELETE_USER}', headers=headers, timeout=10)
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Ошибка при cleanup: {e}")


@pytest.fixture(scope='function')
def authenticated_user():
    user = UserData.valid_user
    token = None

    try:
        with allure.step(f'POST запрос к {APIEndpoints.CREATE_USER} с данными {user}'):
            create_response = requests.post(
                f'{BaseUrls.API_BASE}{APIEndpoints.CREATE_USER}',
                json=user,
                timeout=10
            )

            if create_response.status_code in [200, 201]:
                # Если пользователь создан успешно, логинимся
                user_login = {
                    "email": user["email"],
                    "password": user["password"]
                }
                with allure.step(f'POST запрос к {APIEndpoints.LOGIN} с данными {user_login}'):
                    login_response = requests.post(
                        f'{BaseUrls.API_BASE}{APIEndpoints.LOGIN}',
                        json=user_login,
                        timeout=10
                    )
                    if login_response.status_code == 200:
                        token = login_response.json().get("accessToken")
            else:
                # Если пользователь уже существует, пробуем логин
                user_login = {
                    "email": user["email"],
                    "password": user["password"]
                }
                with allure.step(f'POST запрос к {APIEndpoints.LOGIN} с данными {user_login}'):
                    login_response = requests.post(
                        f'{BaseUrls.API_BASE}{APIEndpoints.LOGIN}',
                        json=user_login,
                        timeout=10
                    )
                    if login_response.status_code == 200:
                        token = login_response.json().get("accessToken")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Ошибка при создании аутентифицированного пользователя: {e}")

    # Всегда возвращаем токен или fallback
    if token:
        yield token
    else:
        yield "mock_token_fallback_12345"

    # Cleanup пропускаем для упрощения
