import pytest
import allure
import requests
from data import HTTPStatus, ResponseMessages, ErrorMessages, UserData
from urls import BaseUrls, APIEndpoints


class UserAuthenticationTests:

    @allure.title('Тестируем логин пользователя.')
    def test_login_user_success(self, create_test_user):
        login_credentials = create_test_user.copy()
        del login_credentials["name"]

        with allure.step(f'POST запрос к {APIEndpoints.LOGIN} с данными {login_credentials}'):
            login_result = requests.post(
                f'{BaseUrls.API_BASE}{APIEndpoints.LOGIN}',
                json=login_credentials
            )
            assert login_result.status_code == HTTPStatus.OK
            assert ResponseMessages.SUCCESS in str(login_result.json())

    @allure.title('Тестируем ошибку входа с неправильными данными.')
    @pytest.mark.parametrize('test_case_id', [1, 2])
    def test_login_user_wrong_credentials(self, create_test_user, test_case_id):
        with allure.step(f'POST запрос к {APIEndpoints.LOGIN} с данными {UserData.invalid_logins[test_case_id]}'):
            login_result = requests.post(
                f'{BaseUrls.API_BASE}{APIEndpoints.LOGIN}',
                json=UserData.invalid_logins[test_case_id]
            )
            assert login_result.status_code == HTTPStatus.UNAUTHORIZED
            assert login_result.json() == ErrorMessages.INVALID_CREDENTIALS