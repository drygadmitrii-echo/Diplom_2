import pytest
import allure
import requests
from data import HTTPStatus, ResponseMessages, ErrorMessages, UserData
from urls import BaseUrls, APIEndpoints


class UserRegistrationTests:

    @allure.title('Тестируем успешное создание нового пользователя.')
    def test_create_user_success(self, generate_user_data):
        with allure.step(f'POST запрос к {APIEndpoints.CREATE_USER} с данными {generate_user_data}'):
            registration_response = requests.post(
                f'{BaseUrls.API_BASE}{APIEndpoints.CREATE_USER}',
                json=generate_user_data
            )
            # API возвращает 200 вместо 201 для успешного создания
            assert registration_response.status_code == 200
            assert registration_response.json().get("success") == True

    @allure.title('Тестируем ошибку повторного создания пользователя с теми же данными.')
    def test_create_user_duplicate(self, create_test_user):
        with allure.step(f'POST запрос к {APIEndpoints.CREATE_USER} с данными {create_test_user}'):
            registration_response = requests.post(
                f'{BaseUrls.API_BASE}{APIEndpoints.CREATE_USER}',
                json=create_test_user
            )
            # API возвращает 403 для дубликата пользователя
            assert registration_response.status_code == 403
            assert registration_response.json().get("success") == False

    @allure.title('Тестируем ошибку создания нового пользователя с неполными данными.')
    @pytest.mark.parametrize('incomplete_user_data', UserData.incomplete_users)
    def test_create_user_missing_data(self, incomplete_user_data):
        with allure.step(f'POST запрос к {APIEndpoints.CREATE_USER} с данными {incomplete_user_data}'):
            registration_response = requests.post(
                f'{BaseUrls.API_BASE}{APIEndpoints.CREATE_USER}',
                json=incomplete_user_data
            )
            # API возвращает 403 для неполных данных
            assert registration_response.status_code == 403
            assert registration_response.json().get("success") == False
