"""Unit tests for existing main.py endpoints (to reach 80%+ total coverage)."""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_home_page():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["message"] == "This is home page"


def test_get_all_items():
    response = client.get("/items")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["count"] >= 2


def test_get_item_found():
    response = client.get("/items/1")
    assert response.status_code == 200
    assert response.json()["status"] == "success"


def test_get_item_not_found():
    response = client.get("/items/9999")
    assert response.status_code == 200
    assert response.json()["status"] == "error"


def test_create_item():
    payload = {"id": 99, "name": "Test Item", "description": "desc", "price": 1.99}
    response = client.post("/items", json=payload)
    assert response.status_code == 200
    assert response.json()["status"] == "success"
