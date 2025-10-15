## Дипломный проект. Задание 2: API-тесты

### Автотесты для проверки API Stellar Burgers

### Реализованные сценарии

Созданы тесты, проверяющие создание пользователя, логин и создание заказа.

### Структура проекта

-- `data.py` - данные для тестирования
-- `conftest.py` - фикстуры тестов
-- `generators.py` - методы генерации тестовых данных

- `tests` - пакет, содержащий тесты.
-- `test_user_registration.py` - тесты создания пользователя
-- `test_user_authentication.py` - тесты логина пользователя
-- `test_order_creation.py` - тесты создания заказа

### Запуск автотестов

Установка зависимостей

`$ pip install -r requirements.txt`

**Запуск автотестов и создание отчета Allure**

`$ pytest .\ --alluredir=allure_results`

**Просмотр отчета Allure**

`$ allure serve allure_results`