"""
Unit tests for main.py (user_story_three)
Covers: GET /health endpoint acceptance criteria + edge cases
"""

import pytest
from fastapi.testclient import TestClient
from main import app, items_db

client = TestClient(app)


# ---------------------------------------------------------------------------
# AC-1: A GET request to /health returns HTTP 200 OK
# ---------------------------------------------------------------------------

class TestHealthEndpointStatus:
    def test_health_returns_200(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_get_method_succeeds(self):
        """Confirm GET specifically works (not other methods)."""
        response = client.get("/health")
        assert response.status_code == 200


# ---------------------------------------------------------------------------
# AC-2: The response body contains the plain string 'service is healthy'
# ---------------------------------------------------------------------------

class TestHealthEndpointBody:
    def test_health_body_is_service_is_healthy(self):
        response = client.get("/health")
        assert response.json() == "service is healthy"

    def test_health_body_exact_match(self):
        response = client.get("/health")
        # Ensure it's exactly the string, not a dict or list
        body = response.json()
        assert isinstance(body, str)
        assert body == "service is healthy"


# ---------------------------------------------------------------------------
# AC-3: The endpoint is accessible without any authentication token or credentials
# ---------------------------------------------------------------------------

class TestHealthNoAuthRequired:
    def test_health_no_auth_header_succeeds(self):
        """No Authorization header — must still return 200."""
        response = client.get("/health", headers={})
        assert response.status_code == 200

    def test_health_no_cookies_succeeds(self):
        """No cookies — must still return 200."""
        response = client.get("/health")
        assert response.status_code != 401
        assert response.status_code != 403


# ---------------------------------------------------------------------------
# AC-4: Content-Type header must be application/json
# ---------------------------------------------------------------------------

class TestHealthContentType:
    def test_health_content_type_is_application_json(self):
        response = client.get("/health")
        assert "application/json" in response.headers.get("content-type", "")


# ---------------------------------------------------------------------------
# Edge Cases
# ---------------------------------------------------------------------------

class TestHealthEdgeCases:
    def test_health_post_returns_405(self):
        response = client.post("/health")
        assert response.status_code == 405

    def test_health_put_returns_405(self):
        response = client.put("/health")
        assert response.status_code == 405

    def test_health_delete_returns_405(self):
        response = client.delete("/health")
        assert response.status_code == 405

    def test_health_patch_returns_405(self):
        response = client.patch("/health")
        assert response.status_code == 405


# ---------------------------------------------------------------------------
# Regression: existing endpoints still work after adding /health
# ---------------------------------------------------------------------------

class TestExistingEndpointsUnchanged:
    def test_home_page_still_works(self):
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "This is home page"

    def test_get_all_items_still_works(self):
        response = client.get("/items")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data
        assert "count" in data

    def test_get_item_by_id_still_works(self):
        response = client.get("/items/1")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"

    def test_create_item_still_works(self):
        payload = {"id": 999, "name": "Test Item", "description": "Test", "price": 1.99}
        response = client.post("/items", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        # Clean up
        items_db[:] = [i for i in items_db if i["name"] != "Test Item"]

    def test_get_item_not_found_returns_error(self):
        response = client.get("/items/99999")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "error"
        assert data["error"] == "Item not found"
