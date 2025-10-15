import os


class Config:
    TESTING = os.getenv('TESTING', 'False').lower() == 'true'
    MOCK_MODE = os.getenv('MOCK_MODE', 'False').lower() == 'true'


class BaseUrls:
    if Config.MOCK_MODE:
        API_BASE = "http://localhost:8000"  # или мок-URL
        WEB_BASE = "http://localhost:8000"
    else:
        API_BASE = "https://stellarburgers.nomoreparties.site"
        WEB_BASE = "https://stellarburgers.nomoreparties.site"