"""
Tests for the /pokemon API endpoints (SCRUM-20).

Covers all acceptance criteria:
  AC1: GET /pokemon/pikachu returns "pikachu"
  AC2: GET /pokemon/charlizad returns "charlizad"
  AC3: GET /pokemon/ash returns "ash"
  AC4: All three endpoints return HTTP 200
  AC5: Endpoints are accessible under the /pokemon path prefix
"""
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# AC4 + AC1: GET /pokemon/pikachu → 200 "pikachu"
# ---------------------------------------------------------------------------
class TestPikachuEndpoint:
    def test_status_200(self):
        response = client.get("/pokemon/pikachu")
        assert response.status_code == 200

    def test_returns_pikachu(self):
        response = client.get("/pokemon/pikachu")
        assert response.json() == "pikachu"

    def test_content_type_json(self):
        response = client.get("/pokemon/pikachu")
        assert "application/json" in response.headers["content-type"]


# ---------------------------------------------------------------------------
# AC4 + AC2: GET /pokemon/charlizad → 200 "charlizad"
# ---------------------------------------------------------------------------
class TestCharlizadEndpoint:
    def test_status_200(self):
        response = client.get("/pokemon/charlizad")
        assert response.status_code == 200

    def test_returns_charlizad(self):
        response = client.get("/pokemon/charlizad")
        assert response.json() == "charlizad"

    def test_content_type_json(self):
        response = client.get("/pokemon/charlizad")
        assert "application/json" in response.headers["content-type"]


# ---------------------------------------------------------------------------
# AC4 + AC3: GET /pokemon/ash → 200 "ash"
# ---------------------------------------------------------------------------
class TestAshEndpoint:
    def test_status_200(self):
        response = client.get("/pokemon/ash")
        assert response.status_code == 200

    def test_returns_ash(self):
        response = client.get("/pokemon/ash")
        assert response.json() == "ash"

    def test_content_type_json(self):
        response = client.get("/pokemon/ash")
        assert "application/json" in response.headers["content-type"]


# ---------------------------------------------------------------------------
# AC5: All endpoints are accessible under the /pokemon path prefix
# ---------------------------------------------------------------------------
class TestPokemonPrefix:
    def test_pikachu_under_pokemon_prefix(self):
        """Path must start with /pokemon/"""
        response = client.get("/pokemon/pikachu")
        assert response.status_code == 200

    def test_charlizad_under_pokemon_prefix(self):
        response = client.get("/pokemon/charlizad")
        assert response.status_code == 200

    def test_ash_under_pokemon_prefix(self):
        response = client.get("/pokemon/ash")
        assert response.status_code == 200

    def test_bare_pokemon_path_returns_404(self):
        """GET /pokemon with no sub-path should 404 (no route registered)."""
        response = client.get("/pokemon")
        assert response.status_code == 404

    def test_unknown_sub_path_returns_404(self):
        """GET /pokemon/bulbasaur should return 404."""
        response = client.get("/pokemon/bulbasaur")
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# Edge-case: router does not shadow pre-existing routes
# ---------------------------------------------------------------------------
class TestExistingRoutesUnaffected:
    def test_home_still_works(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_items_still_works(self):
        response = client.get("/items")
        assert response.status_code == 200
