#!/usr/bin/env python3
"""
Полный запуск ВСЕХ тестов дипломного проекта с реальным API
"""

import subprocess
import sys
import os
import requests
from urls import BaseUrls


def check_api_availability():
    """Проверяет доступность API перед запуском тестов"""
    print("🔍 Проверка доступности API...")
    try:
        response = requests.get(BaseUrls.API_BASE, timeout=10)
        print(f"✅ API доступен! Статус: {response.status_code}")
        return True
    except Exception as e:
        print(f"❌ API недоступен: {e}")
        return False


def run_all_tests():
    """Запускает ВСЕ тесты проекта"""

    print("🚀 ЗАПУСК ПОЛНОЙ ПРОВЕРКИ ДИПЛОМНОГО ПРОЕКТА")
    print("=" * 60)

    # Проверяем доступность API
    api_available = check_api_availability()

    # Базовые тесты (всегда запускаются)
    test_files = [
        "test_imports.py",
        "test_modules.py",
        "test_with_mocks.py",
        "test_all_mocked.py"
    ]

    # Если API доступно, добавляем реальные тесты из папки tests/
    if api_available:
        print("🎯 API доступен! Запускаем ВСЕ тесты...")
        test_files.extend([
            "tests/test_create_user.py",
            "tests/test_login_user.py",
            "tests/test_create_order.py"
        ])
    else:
        print("⚠️  API недоступен. Запускаем только мок-тесты...")

    # Создаем директорию для результатов
    os.makedirs("allure-results", exist_ok=True)

    print("📋 Будет выполнена проверка:")
    for test_file in test_files:
        print(f"   • {test_file}")
    print("=" * 60)

    # Запускаем тесты
    result = subprocess.run([
        "pytest",
        *test_files,
        "-v",
        "--alluredir=allure-results",
        "--tb=short",
        "--strict-markers"
    ], capture_output=False)

    print("=" * 60)

    if result.returncode == 0:
        print("🎉 ВСЕ ТЕСТЫ ПРОШЛИ УСПЕШНО!")
        print("✅ Все модули работают корректно")
        print("✅ Импорты без ошибок")
        print("✅ API логика проверена")
        print("✅ Генераторы данных работают")
        if api_available:
            print("✅ Реальные API тесты выполнены")
        else:
            print("⚠️  Реальные API тесты пропущены (API недоступно)")
    else:
        print("❌ Некоторые тесты не прошли")

    print("\n📊 Для просмотра детального отчета выполните:")
    print("   allure serve allure-results")

    return result.returncode


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)