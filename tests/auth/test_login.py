import pytest
import requests

def test_admin_login():
    # Попытка входа с правильными кредами
    response = requests.post(
        "https://localhost:2443/login",
        json={"username": "admin", "password": "admin"},
        verify=False  # Игнорируем SSL ошибки для тестов
    )
    assert response.status_code == 200
    assert "token" in response.json()

def test_wrong_password():
    # Неправильный пароль
    response = requests.post(
        "https://localhost:2443/login",
        json={"username": "admin", "password": "wrong"},
        verify=False
    )
    assert response.status_code == 401
