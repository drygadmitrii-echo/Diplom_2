from unittest.mock import Mock, patch
import json


class MockResponse:
    def __init__(self, status_code, json_data=None, text=None, headers=None):
        self.status_code = status_code
        self._json_data = json_data or {}
        self.text = text or json.dumps(json_data)
        self.headers = headers or {}

    def json(self):
        return self._json_data


# Мок-данные для успешных ответов
def mock_successful_create_user():
    return MockResponse(201, {
        "success": True,
        "user": {
            "email": "test@example.com",
            "name": "Test User"
        },
        "accessToken": "mock_token_12345"
    })


def mock_successful_login():
    return MockResponse(200, {
        "success": True,
        "accessToken": "mock_token_12345",
        "refreshToken": "mock_refresh_token"
    })


def mock_successful_order():
    return MockResponse(200, {
        "success": True,
        "name": "Mock Burger",
        "order": {"number": 12345}
    })


# Мок-данные для ошибок
def mock_user_exists_error():
    return MockResponse(403, {
        "success": False,
        "message": "User already exists"
    })


def mock_unauthorized_error():
    return MockResponse(401, {
        "success": False,
        "message": "email or password are incorrect"
    })


def mock_missing_fields_error():
    return MockResponse(403, {
        "success": False,
        "message": "Email, password and name are required fields"
    })