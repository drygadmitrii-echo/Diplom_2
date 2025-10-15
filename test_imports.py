import pytest
import allure
import sys
import importlib


@allure.title("Тест импорта всех модулей проекта")
class TestProjectImports:
    """Тесты для проверки что все модули импортируются без ошибок"""

    def test_import_data(self):
        """Проверка импорта data.py"""
        try:
            from data import HTTPStatus, ResponseMessages, ErrorMessages, UserData, OrderData
            assert True
        except ImportError as e:
            pytest.fail(f"Ошибка импорта data.py: {e}")

    def test_import_generators(self):
        """Проверка импорта generators.py"""
        try:
            from generators import generate_email, generate_secure_password, generate_username, generate_comment
            assert True
        except ImportError as e:
            pytest.fail(f"Ошибка импорта generators.py: {e}")

    def test_import_urls(self):
        """Проверка импорта urls.py"""
        try:
            from urls import BaseUrls, APIEndpoints
            assert True
        except ImportError as e:
            pytest.fail(f"Ошибка импорта urls.py: {e}")

    def test_import_conftest_fixtures(self):
        """Проверка что фикстуры доступны"""
        try:
            # Эти фикстуры должны быть доступны после импорта conftest.py
            import conftest
            assert hasattr(conftest, 'generate_user_data')
            assert hasattr(conftest, 'create_test_user')
            assert hasattr(conftest, 'authenticated_user')
        except Exception as e:
            pytest.fail(f"Ошибка доступа к фикстурам: {e}")

    def test_all_modules_importable(self):
        """Проверка что все основные модули могут быть импортированы"""
        modules = ['data', 'generators', 'urls', 'conftest']

        for module_name in modules:
            try:
                importlib.import_module(module_name)
                assert True
            except Exception as e:
                pytest.fail(f"Модуль {module_name} не может быть импортирован: {e}")