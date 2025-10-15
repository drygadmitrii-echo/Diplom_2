import pytest
import allure
import requests
from data import HTTPStatus, ResponseMessages, ErrorMessages, UserData, OrderData
from urls import BaseUrls, APIEndpoints
from generators import generate_email, generate_secure_password, generate_username, generate_comment


class TestDataModule:
    """Тесты для data.py"""

    @allure.title("Проверка констант HTTP статусов")
    def test_http_status_constants(self):
        assert HTTPStatus.CREATED == 201
        assert HTTPStatus.OK == 200
        assert HTTPStatus.BAD_REQUEST == 400
        assert HTTPStatus.UNAUTHORIZED == 401
        assert HTTPStatus.FORBIDDEN == 403
        assert HTTPStatus.NOT_FOUND == 404
        assert HTTPStatus.INTERNAL_ERROR == 500

    @allure.title("Проверка структуры UserData")
    def test_user_data_structure(self):
        user = UserData.valid_user
        assert "email" in user
        assert "password" in user
        assert "name" in user
        assert isinstance(user["email"], str)
        assert isinstance(user["password"], str)
        assert isinstance(user["name"], str)

    @allure.title("Проверка incomplete_users")
    def test_incomplete_users(self):
        assert len(UserData.incomplete_users) == 3
        for user in UserData.incomplete_users:
            assert "email" in user
            assert "password" in user
            assert "name" in user

    @allure.title("Проверка OrderData")
    def test_order_data(self):
        assert "ingredients" in OrderData.valid_order
        assert "ingredients" in OrderData.empty_order
        assert "ingredients" in OrderData.invalid_ingredients
        assert isinstance(OrderData.valid_order["ingredients"], list)


class TestGeneratorsModule:
    """Тесты для generators.py"""

    @allure.title("Проверка генерации email")
    def test_generate_email(self):
        email = generate_email()
        assert "@" in email
        assert "." in email
        # Проверим несколько разных email
        emails = [generate_email() for _ in range(5)]
        assert len(set(emails)) == 5  # Все email должны быть уникальными

    @allure.title("Проверка генерации пароля")
    def test_generate_secure_password(self):
        password = generate_secure_password()
        assert len(password) >= 10
        # Проверим что пароль содержит разные типы символов
        assert any(c.isalpha() for c in password)
        assert any(c.isdigit() for c in password)

    @allure.title("Проверка генерации имени пользователя")
    def test_generate_username(self):
        username = generate_username()
        assert isinstance(username, str)
        assert len(username) > 0

    @allure.title("Проверка генерации комментария")
    def test_generate_comment(self):
        comment = generate_comment()
        assert isinstance(comment, str)
        assert len(comment) > 0


class TestUrlsModule:
    """Тесты для urls.py"""

    @allure.title("Проверка базовых URL")
    def test_base_urls(self):
        assert BaseUrls.API_BASE == "https://stellarburgers.education-services.ru"
        assert BaseUrls.WEB_BASE == "https://stellarburgers.education-services.ru"

    @allure.title("Проверка эндпоинтов API")
    def test_api_endpoints(self):
        endpoints = [
            APIEndpoints.CREATE_USER,
            APIEndpoints.LOGIN,
            APIEndpoints.LOGOUT,
            APIEndpoints.DELETE_USER,
            APIEndpoints.CREATE_ORDER,
            APIEndpoints.GET_ORDERS,
            APIEndpoints.USER_INFO,
            APIEndpoints.UPDATE_USER
        ]

        for endpoint in endpoints:
            assert isinstance(endpoint, str)
            assert endpoint.startswith("/")


class TestConftestFixtures:
    """Тесты для фикстур из conftest.py"""

    @allure.title("Проверка фикстуры generate_user_data")
    def test_generate_user_data_fixture(self, generate_user_data):
        user = generate_user_data
        assert "email" in user
        assert "password" in user
        assert "name" in user

    @allure.title("Проверка фикстуры create_test_user")
    def test_create_test_user_fixture(self, create_test_user):
        user = create_test_user
        assert "email" in user
        assert "password" in user
        assert "name" in user

    @allure.title("Проверка фикстуры authenticated_user")
    def test_authenticated_user_fixture(self, authenticated_user):
        token = authenticated_user
        assert isinstance(token, str)
        assert len(token) > 0


class TestIntegration:
    """Интеграционные тесты"""

    @allure.title("Интеграционный тест: генерация данных -> создание запроса")
    def test_data_generation_integration(self):
        # Генерируем тестовые данные
        email = generate_email()
        password = generate_secure_password()
        name = generate_username()

        # Создаем пользователя
        user_data = {
            "email": email,
            "password": password,
            "name": name
        }

        # Проверяем структуру
        assert all(key in user_data for key in ["email", "password", "name"])
        assert "@" in user_data["email"]
        assert len(user_data["password"]) >= 10

    @allure.title("Проверка формирования полного URL")
    def test_url_formation(self):
        full_url = f"{BaseUrls.API_BASE}{APIEndpoints.CREATE_USER}"
        expected_url = "https://stellarburgers.education-services.ru/api/auth/register"
        assert full_url == expected_url


class TestErrorMessages:
    """Тесты для сообщений об ошибках"""

    @allure.title("Проверка структуры сообщений об ошибках")
    def test_error_messages_structure(self):
        errors = [
            ErrorMessages.USER_EXISTS,
            ErrorMessages.MISSING_FIELDS,
            ErrorMessages.INVALID_CREDENTIALS,
            ErrorMessages.NO_INGREDIENTS
        ]

        for error in errors:
            assert "success" in error
            assert "message" in error
            assert error["success"] == False
            assert isinstance(error["message"], str)
            assert len(error["message"]) > 0