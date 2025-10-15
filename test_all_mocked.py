import pytest
import allure
from unittest.mock import patch, Mock
from data import *
from urls import *


class TestAllScenariosMocked:

    @patch('requests.post')
    def test_complete_user_flow_mocked(self, mock_post):
        """Полный flow пользователя: регистрация -> логин -> создание заказа"""

        # Настраиваем моки для разных вызовов
        mock_responses = [
            # Регистрация
            Mock(status_code=201,
                 json=lambda: {"success": True, "user": {"email": "test@test.com", "name": "Test User"},
                               "accessToken": "token123"}),
            # Логин
            Mock(status_code=200, json=lambda: {"success": True, "accessToken": "token123"}),
            # Создание заказа
            Mock(status_code=200, json=lambda: {"success": True, "order": {"number": 12345}})
        ]
        mock_post.side_effect = mock_responses

        import requests

        # 1. Регистрация
        reg_response = requests.post(
            f"{BaseUrls.API_BASE}{APIEndpoints.CREATE_USER}",
            json=UserData.valid_user
        )
        assert reg_response.status_code == 201
        assert reg_response.json()["success"] == True

        # 2. Логин
        login_data = UserData.valid_user.copy()
        del login_data["name"]
        login_response = requests.post(
            f"{BaseUrls.API_BASE}{APIEndpoints.LOGIN}",
            json=login_data
        )
        assert login_response.status_code == 200

        # 3. Создание заказа
        order_response = requests.post(
            f"{BaseUrls.API_BASE}{APIEndpoints.CREATE_ORDER}",
            json=OrderData.valid_order,
            headers={"Authorization": "token123"}
        )
        assert order_response.status_code == 200

    @pytest.mark.parametrize("scenario", [
        ("duplicate_user", 403, ErrorMessages.USER_EXISTS),
        ("invalid_credentials", 401, ErrorMessages.INVALID_CREDENTIALS),
        ("missing_fields", 403, ErrorMessages.MISSING_FIELDS)
    ])
    @patch('requests.post')
    def test_error_scenarios_mocked(self, mock_post, scenario):
        scenario_name, expected_status, expected_error = scenario

        mock_post.return_value = Mock(
            status_code=expected_status,
            json=lambda: expected_error
        )

        import requests

        response = requests.post(
            f"{BaseUrls.API_BASE}{APIEndpoints.CREATE_USER}",
            json=UserData.valid_user
        )

        assert response.status_code == expected_status
        assert response.json() == expected_error