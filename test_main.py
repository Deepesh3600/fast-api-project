"""Unit tests for main.py — covers all acceptance criteria and edge cases for GET /12345."""

import json
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app, raise_server_exceptions=True)


# ── Acceptance Criteria ────────────────────────────────────────────────────────

class TestGetNumericEndpointAC:
    """AC1-AC4: Core acceptance criteria from analysis.json."""

    def test_ac1_returns_200_ok(self):
        """AC1: A GET request to /12345 returns HTTP 200 OK."""
        response = client.get("/12345")
        assert response.status_code == 200

    def test_ac2_response_body_is_exactly_12345678910(self):
        """AC2: The response body is exactly 12345678910."""
        response = client.get("/12345")
        assert response.json() == 12345678910

    def test_ac3_no_auth_required(self):
        """AC3: Endpoint is publicly accessible without any auth token."""
        # No Authorization header — must succeed
        response = client.get("/12345", headers={})
        assert response.status_code == 200

    def test_ac4_content_type_is_application_json(self):
        """AC4: The Content-Type header of the response is application/json."""
        response = client.get("/12345")
        assert "application/json" in response.headers.get("content-type", "")


# ── Edge Cases ─────────────────────────────────────────────────────────────────

class TestGetNumericEndpointEdgeCases:
    """Edge cases from analysis.json."""

    def test_post_returns_405(self):
        """Non-GET POST to /12345 should return 405 Method Not Allowed."""
        response = client.post("/12345")
        assert response.status_code == 405

    def test_put_returns_405(self):
        """Non-GET PUT to /12345 should return 405 Method Not Allowed."""
        response = client.put("/12345")
        assert response.status_code == 405

    def test_delete_returns_405(self):
        """Non-GET DELETE to /12345 should return 405 Method Not Allowed."""
        response = client.delete("/12345")
        assert response.status_code == 405

    def test_patch_returns_405(self):
        """Non-GET PATCH to /12345 should return 405 Method Not Allowed."""
        response = client.patch("/12345")
        assert response.status_code == 405

    def test_query_params_ignored_200(self):
        """Requests with query params /12345?foo=bar should still return 200."""
        response = client.get("/12345?foo=bar&baz=qux")
        assert response.status_code == 200
        assert response.json() == 12345678910

    def test_extra_path_segment_returns_404(self):
        """Extra path segments /12345/extra should return 404."""
        response = client.get("/12345/extra")
        assert response.status_code == 404

    def test_value_is_number_not_string(self):
        """Numeric value must be serialised as a JSON number, not a string."""
        response = client.get("/12345")
        raw_body = response.text.strip()
        # Must be parseable as JSON number (not quoted)
        parsed = json.loads(raw_body)
        assert isinstance(parsed, int)
        assert not raw_body.startswith('"')

    def test_no_route_conflict_with_items(self):
        """Existing /items endpoint must still work (no route conflict)."""
        response = client.get("/items")
        assert response.status_code == 200

    def test_no_route_conflict_with_root(self):
        """Existing / endpoint must still work."""
        response = client.get("/")
        assert response.status_code == 200

    def test_no_route_conflict_with_item_by_id(self):
        """Existing /items/{item_id} endpoint must still work."""
        response = client.get("/items/1")
        assert response.status_code == 200
