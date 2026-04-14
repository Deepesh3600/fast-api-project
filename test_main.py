"""Unit tests for main.py — covers all endpoints including the new GET /random endpoint."""
import pytest
from fastapi.testclient import TestClient

from main import app, items_db

client = TestClient(app)


# ── Fixture ──────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def reset_items_db():
    """Reset in-memory DB to its original two-item state before each test."""
    items_db.clear()
    items_db.extend([
        {"id": 1, "name": "Item 1", "description": "First item", "price": 9.99},
        {"id": 2, "name": "Item 2", "description": "Second item", "price": 19.99},
    ])
    yield


# ── GET / ─────────────────────────────────────────────────────────────────────

class TestHomePage:
    def test_returns_200(self):
        r = client.get("/")
        assert r.status_code == 200

    def test_response_body(self):
        r = client.get("/")
        assert r.json() == {"message": "This is home page", "status": "success"}


# ── GET /items ────────────────────────────────────────────────────────────────

class TestGetAllItems:
    def test_returns_200(self):
        r = client.get("/items")
        assert r.status_code == 200

    def test_response_contains_items(self):
        r = client.get("/items")
        data = r.json()
        assert "items" in data
        assert "count" in data
        assert data["count"] == 2

    def test_count_reflects_actual_length(self):
        items_db.append({"id": 3, "name": "X", "description": None, "price": 1.0})
        r = client.get("/items")
        assert r.json()["count"] == 3


# ── GET /items/{item_id} ──────────────────────────────────────────────────────

class TestGetItem:
    def test_existing_item_returns_200(self):
        r = client.get("/items/1")
        assert r.status_code == 200

    def test_existing_item_body(self):
        r = client.get("/items/1")
        data = r.json()
        assert data["status"] == "success"
        assert data["data"]["id"] == 1

    def test_missing_item_returns_error(self):
        r = client.get("/items/999")
        assert r.status_code == 200  # FastAPI returns 200 with error payload
        assert r.json()["status"] == "error"


# ── POST /items ───────────────────────────────────────────────────────────────

class TestCreateItem:
    def test_create_returns_200(self):
        payload = {"id": 0, "name": "New", "description": "desc", "price": 5.0}
        r = client.post("/items", json=payload)
        assert r.status_code == 200

    def test_create_appends_to_db(self):
        payload = {"id": 0, "name": "New", "description": "desc", "price": 5.0}
        client.post("/items", json=payload)
        assert len(items_db) == 3

    def test_create_response_body(self):
        payload = {"id": 0, "name": "New", "description": "desc", "price": 5.0}
        r = client.post("/items", json=payload)
        data = r.json()
        assert data["status"] == "success"
        assert data["data"]["name"] == "New"

    def test_auto_increment_id(self):
        payload = {"id": 0, "name": "Auto", "description": "desc", "price": 1.0}
        r = client.post("/items", json=payload)
        assert r.json()["data"]["id"] == 3


# ── GET /random ───────────────────────────────────────────────────────────────
# These tests directly map to the acceptance criteria.

class TestGetRandom:
    # AC1: A new GET endpoint is available at /random
    def test_endpoint_exists_and_returns_200(self):
        r = client.get("/random")
        assert r.status_code == 200

    # AC2: The endpoint returns the plain string "random" with a 200 OK status
    def test_response_body_is_string_random(self):
        r = client.get("/random")
        assert r.json() == "random"

    # AC2 (content-type): response Content-Type must be application/json
    def test_content_type_is_json(self):
        r = client.get("/random")
        assert "application/json" in r.headers["content-type"]

    # AC3: No authentication or authorization is required
    def test_no_auth_required(self):
        """Endpoint must be accessible without any Authorization header."""
        r = client.get("/random")  # no auth header
        assert r.status_code == 200

    # Edge-case: non-GET methods should return 405
    def test_post_returns_405(self):
        r = client.post("/random")
        assert r.status_code == 405

    def test_put_returns_405(self):
        r = client.put("/random")
        assert r.status_code == 405

    def test_delete_returns_405(self):
        r = client.delete("/random")
        assert r.status_code == 405

    # Edge-case: determinism — multiple concurrent-style calls return same value
    def test_deterministic_response(self):
        responses = {client.get("/random").json() for _ in range(5)}
        assert responses == {"random"}
