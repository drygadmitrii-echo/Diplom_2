#!/usr/bin/env python3
"""
Запуск тестов для дипломного проекта Stellar Burgers API
"""

import subprocess
import sys
import os


def run_tests():
    """Запускает все тесты и генерирует отчет"""

    print("🚀 Запуск тестов дипломного проекта...")
    print("=" * 50)

    # Создаем директорию для результатов Allure если ее нет
    os.makedirs("allure-results", exist_ok=True)

    # Запускаем тесты
    test_files = ["test_with_mocks.py", "test_all_mocked.py"]

    result = subprocess.run([
        "pytest",
        *test_files,
        "-v",
        "--alluredir=allure-results",
        "--tb=short"
    ], capture_output=False)

    print("=" * 50)

    if result.returncode == 0:
        print("✅ Все тесты прошли успешно!")
        print("\n📊 Для просмотра отчета Allure выполните:")
        print("   allure serve allure-results")
    else:
        print("❌ Некоторые тесты не прошли")

    return result.returncode


if __name__ == "__main__":
    sys.exit(run_tests())