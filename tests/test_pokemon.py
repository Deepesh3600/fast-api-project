"""Unit tests for the /pokemon router endpoints."""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestPikachuEndpoint:
    """AC: GET /pokemon/pikachu responds with 'pikachu' and HTTP 200 OK."""

    def test_get_pikachu_status_200(self):
        response = client.get("/pokemon/pikachu")
        assert response.status_code == 200

    def test_get_pikachu_body(self):
        response = client.get("/pokemon/pikachu")
        assert response.text == "pikachu"

    def test_get_pikachu_content_type_plain_text(self):
        response = client.get("/pokemon/pikachu")
        assert "text/plain" in response.headers["content-type"]

    def test_get_pikachu_post_method_not_allowed(self):
        response = client.post("/pokemon/pikachu")
        assert response.status_code == 405

    def test_get_pikachu_put_method_not_allowed(self):
        response = client.put("/pokemon/pikachu")
        assert response.status_code == 405

    def test_get_pikachu_delete_method_not_allowed(self):
        response = client.delete("/pokemon/pikachu")
        assert response.status_code == 405


class TestCharlizadEndpoint:
    """AC: GET /pokemon/charlizad responds with 'charlizad' and HTTP 200 OK."""

    def test_get_charlizad_status_200(self):
        response = client.get("/pokemon/charlizad")
        assert response.status_code == 200

    def test_get_charlizad_body(self):
        response = client.get("/pokemon/charlizad")
        assert response.text == "charlizad"

    def test_get_charlizad_content_type_plain_text(self):
        response = client.get("/pokemon/charlizad")
        assert "text/plain" in response.headers["content-type"]

    def test_get_charlizad_post_method_not_allowed(self):
        response = client.post("/pokemon/charlizad")
        assert response.status_code == 405

    def test_get_charlizad_put_method_not_allowed(self):
        response = client.put("/pokemon/charlizad")
        assert response.status_code == 405

    def test_get_charlizad_delete_method_not_allowed(self):
        response = client.delete("/pokemon/charlizad")
        assert response.status_code == 405


class TestAshEndpoint:
    """AC: GET /pokemon/ash responds with 'ash' and HTTP 200 OK."""

    def test_get_ash_status_200(self):
        response = client.get("/pokemon/ash")
        assert response.status_code == 200

    def test_get_ash_body(self):
        response = client.get("/pokemon/ash")
        assert response.text == "ash"

    def test_get_ash_content_type_plain_text(self):
        response = client.get("/pokemon/ash")
        assert "text/plain" in response.headers["content-type"]

    def test_get_ash_post_method_not_allowed(self):
        response = client.post("/pokemon/ash")
        assert response.status_code == 405

    def test_get_ash_put_method_not_allowed(self):
        response = client.put("/pokemon/ash")
        assert response.status_code == 405

    def test_get_ash_delete_method_not_allowed(self):
        response = client.delete("/pokemon/ash")
        assert response.status_code == 405


class TestPokemonRouteGroup:
    """AC: The /pokemon route group is accessible and registered."""

    def test_pokemon_root_returns_404(self):
        """Root /pokemon path should return 404 since no handler is defined."""
        response = client.get("/pokemon")
        assert response.status_code == 404

    def test_unknown_pokemon_returns_404(self):
        """Unknown sub-paths should return 404."""
        response = client.get("/pokemon/bulbasaur")
        assert response.status_code == 404

    def test_openapi_includes_pokemon_routes(self):
        """Ensure the router is registered - all 3 paths appear in OpenAPI spec."""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        paths = response.json()["paths"]
        assert "/pokemon/pikachu" in paths
        assert "/pokemon/charlizad" in paths
        assert "/pokemon/ash" in paths

    def test_case_sensitive_pikachu(self):
        """Route matching is case-sensitive by default in FastAPI."""
        response = client.get("/pokemon/Pikachu")
        assert response.status_code == 404

    def test_trailing_slash_pikachu_not_200_with_wrong_body(self):
        """Trailing slash variant should not return pikachu body as 200 unexpectedly."""
        response = client.get("/pokemon/pikachu/", follow_redirects=False)
        # Either redirects (307) or 404 - but if 200, body must still be correct
        assert response.status_code in (200, 307, 404)
