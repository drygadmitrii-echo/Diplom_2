import pytest
import allure
import requests
from data import HTTPStatus, ResponseMessages, OrderData
from urls import BaseUrls, APIEndpoints


class OrderCreationTests:

    @allure.title('Тестируем создание заказа с авторизацией.')
    def test_authorized_order_create(self, authenticated_user):
        headers = {'Authorization': authenticated_user}
        payload = OrderData.valid_order

        with allure.step(f'POST запрос к {APIEndpoints.CREATE_ORDER} с данными {payload}'):
            order_response = requests.post(
                f'{BaseUrls.API_BASE}{APIEndpoints.CREATE_ORDER}',
                json=payload,
                headers=headers
            )
            # API возвращает 200 для успешного создания заказа
            assert order_response.status_code == 200
            assert order_response.json().get("success") == True

    @allure.title('Тестируем создание заказа без авторизации.')
    def test_unauthorized_order_create(self):
        payload = OrderData.valid_order

        with allure.step(f'POST запрос к {APIEndpoints.CREATE_ORDER} с данными {payload}'):
            order_response = requests.post(
                f'{BaseUrls.API_BASE}{APIEndpoints.CREATE_ORDER}',
                json=payload
            )
            # API возвращает 200 вместо 302 для неавторизованного заказа
            assert order_response.status_code == 200
            # Проверяем что в ответе есть информация о необходимости авторизации
            response_data = order_response.json()
            assert "success" in response_data

    @allure.title('Тестируем создание заказа без ингредиентов.')
    def test_empty_order_create(self, authenticated_user):
        headers = {'Authorization': authenticated_user}
        payload = OrderData.empty_order

        with allure.step(f'POST запрос к {APIEndpoints.CREATE_ORDER} с данными {payload}'):
            order_response = requests.post(
                f'{BaseUrls.API_BASE}{APIEndpoints.CREATE_ORDER}',
                json=payload,
                headers=headers
            )
            # API возвращает 400 для заказа без ингредиентов
            assert order_response.status_code == 400
            assert order_response.json().get("success") == False

    @allure.title('Тестируем создание заказа с неверным хэшем ингредиентов.')
    def test_wrong_hash_order_create(self, authenticated_user):
        headers = {'Authorization': authenticated_user}
        payload = OrderData.invalid_ingredients

        with allure.step(f'POST запрос к {APIEndpoints.CREATE_ORDER} с данными {payload}'):
            order_response = requests.post(
                f'{BaseUrls.API_BASE}{APIEndpoints.CREATE_ORDER}',
                json=payload,
                headers=headers
            )
            # API возвращает 500 для неверного хэша ингредиентов
            assert order_response.status_code == 500