"""
Unit and integration tests for main.py
Covers the GET /authentication endpoint and existing routes.
"""
import json
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ──────────────────────────────────────────────────────────────────────────────
# AC-1: A new GET endpoint is available at /authentication
# ──────────────────────────────────────────────────────────────────────────────
class TestAuthenticationEndpointExists:
    def test_get_authentication_returns_200(self):
        response = client.get("/authentication")
        assert response.status_code == 200

    def test_get_authentication_is_reachable_without_credentials(self):
        """No auth headers needed – endpoint must be publicly accessible (AC-3)."""
        response = client.get("/authentication")
        assert response.status_code != 401
        assert response.status_code != 403


# ──────────────────────────────────────────────────────────────────────────────
# AC-2: Returns the plain string "authenticated" with 200 OK
# ──────────────────────────────────────────────────────────────────────────────
class TestAuthenticationResponse:
    def test_response_body_is_exact_string_authenticated(self):
        response = client.get("/authentication")
        # JSONResponse(content="authenticated") serialises to the JSON string "authenticated"
        assert response.json() == "authenticated"

    def test_response_body_is_not_wrapped_in_object(self):
        response = client.get("/authentication")
        body = response.json()
        assert not isinstance(body, dict), "Body must be a plain string, not an object"

    def test_response_content_type_is_application_json(self):
        response = client.get("/authentication")
        assert "application/json" in response.headers["content-type"]

    def test_response_status_code_is_200(self):
        response = client.get("/authentication")
        assert response.status_code == 200


# ──────────────────────────────────────────────────────────────────────────────
# AC-3: No authentication / authorisation required
# ──────────────────────────────────────────────────────────────────────────────
class TestNoAuthRequired:
    def test_no_auth_header_required(self):
        """Plain request without any Authorization header must succeed."""
        response = client.get("/authentication", headers={})
        assert response.status_code == 200

    def test_invalid_auth_header_still_succeeds(self):
        """Even a bogus auth header must not block this public endpoint."""
        response = client.get("/authentication", headers={"Authorization": "Bearer invalid-token"})
        assert response.status_code == 200


# ──────────────────────────────────────────────────────────────────────────────
# Edge cases
# ──────────────────────────────────────────────────────────────────────────────
class TestAuthenticationEdgeCases:
    def test_post_returns_405(self):
        response = client.post("/authentication")
        assert response.status_code == 405

    def test_put_returns_405(self):
        response = client.put("/authentication")
        assert response.status_code == 405

    def test_delete_returns_405(self):
        response = client.delete("/authentication")
        assert response.status_code == 405

    def test_raw_body_text_equals_json_encoded_string(self):
        response = client.get("/authentication")
        # The raw text must be the JSON encoding of the string "authenticated"
        assert response.text == '"authenticated"'


# ──────────────────────────────────────────────────────────────────────────────
# Existing routes – regression tests (ensure nothing was broken)
# ──────────────────────────────────────────────────────────────────────────────
class TestExistingRoutes:
    def test_home_page_returns_200(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_get_all_items_returns_200(self):
        response = client.get("/items")
        assert response.status_code == 200
        assert "items" in response.json()

    def test_get_item_by_id_returns_200(self):
        response = client.get("/items/1")
        assert response.status_code == 200
        assert response.json()["data"]["id"] == 1

    def test_get_nonexistent_item_returns_error(self):
        response = client.get("/items/9999")
        assert response.json()["status"] == "error"

    def test_create_item_returns_200(self):
        payload = {"id": 99, "name": "Test Item", "description": "desc", "price": 5.0}
        response = client.post("/items", json=payload)
        assert response.status_code == 200
        assert response.json()["status"] == "success"
