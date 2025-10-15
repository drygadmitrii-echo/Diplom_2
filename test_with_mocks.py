import pytest
import allure
from unittest.mock import patch
from data import *
from urls import *
from mocks import *


class TestUserRegistrationWithMocks:

    @allure.title('Тестируем успешное создание нового пользователя (мок)')
    @patch('requests.post')
    def test_create_user_success_mock(self, mock_post, generate_user_data):
        # Настраиваем мок
        mock_post.return_value = mock_successful_create_user()

        # Импортируем requests здесь, чтобы мок сработал
        import requests

        with allure.step(f'POST запрос к {APIEndpoints.CREATE_USER} с данными {generate_user_data}'):
            registration_response = requests.post(
                f'{BaseUrls.API_BASE}{APIEndpoints.CREATE_USER}',
                json=generate_user_data
            )

            assert registration_response.status_code == HTTPStatus.CREATED
            assert registration_response.json()["success"] == True
            assert "accessToken" in registration_response.json()

    @allure.title('Тестируем ошибку повторного создания пользователя (мок)')
    @patch('requests.post')
    def test_create_user_duplicate_mock(self, mock_post):
        # Настраиваем мок для ошибки существующего пользователя
        mock_post.return_value = mock_user_exists_error()

        import requests
        user_data = UserData.valid_user

        with allure.step(f'POST запрос к {APIEndpoints.CREATE_USER} с данными {user_data}'):
            registration_response = requests.post(
                f'{BaseUrls.API_BASE}{APIEndpoints.CREATE_USER}',
                json=user_data
            )

            assert registration_response.status_code == HTTPStatus.FORBIDDEN
            assert registration_response.json() == ErrorMessages.USER_EXISTS


class TestOrderCreationWithMocks:

    @allure.title('Тестируем создание заказа с авторизацией (мок)')
    @patch('requests.post')
    def test_authorized_order_create_mock(self, mock_post):
        # Настраиваем мок для успешного создания заказа
        mock_post.return_value = mock_successful_order()

        import requests
        headers = {'Authorization': 'mock_token'}
        payload = OrderData.valid_order

        with allure.step(f'POST запрос к {APIEndpoints.CREATE_ORDER} с данными {payload}'):
            order_response = requests.post(
                f'{BaseUrls.API_BASE}{APIEndpoints.CREATE_ORDER}',
                json=payload,
                headers=headers
            )

            assert order_response.status_code == HTTPStatus.OK
            assert order_response.json()["success"] == True