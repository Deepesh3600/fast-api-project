"""Unit and integration tests for the /pokemon router."""
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Acceptance Criteria tests
# ---------------------------------------------------------------------------

class TestPokemonKnownNames:
    """AC: GET /pokemon/{name} returns 200 + {"name": "<name>"} for known pokemon."""

    def test_pikachu_returns_200(self):
        response = client.get("/pokemon/pikachu")
        assert response.status_code == 200

    def test_pikachu_returns_correct_body(self):
        response = client.get("/pokemon/pikachu")
        assert response.json() == {"name": "pikachu"}

    def test_charlizad_returns_200(self):
        response = client.get("/pokemon/charlizad")
        assert response.status_code == 200

    def test_charlizad_returns_correct_body(self):
        response = client.get("/pokemon/charlizad")
        assert response.json() == {"name": "charlizad"}

    def test_ash_returns_200(self):
        response = client.get("/pokemon/ash")
        assert response.status_code == 200

    def test_ash_returns_correct_body(self):
        response = client.get("/pokemon/ash")
        assert response.json() == {"name": "ash"}


class TestPokemonCaseInsensitivity:
    """Case-insensitive matching: Pikachu -> pikachu."""

    def test_pikachu_uppercase(self):
        response = client.get("/pokemon/PIKACHU")
        assert response.status_code == 200
        assert response.json() == {"name": "pikachu"}

    def test_pikachu_mixed_case(self):
        response = client.get("/pokemon/Pikachu")
        assert response.status_code == 200
        assert response.json() == {"name": "pikachu"}

    def test_ash_uppercase(self):
        response = client.get("/pokemon/ASH")
        assert response.status_code == 200
        assert response.json() == {"name": "ash"}

    def test_charlizad_mixed_case(self):
        response = client.get("/pokemon/ChArLiZaD")
        assert response.status_code == 200
        assert response.json() == {"name": "charlizad"}


class TestPokemonUnknownName:
    """AC (edge case): Unknown pokemon name -> 404."""

    def test_unknown_pokemon_returns_404(self):
        response = client.get("/pokemon/bulbasaur")
        assert response.status_code == 404

    def test_unknown_pokemon_has_detail(self):
        response = client.get("/pokemon/bulbasaur")
        body = response.json()
        assert "detail" in body

    def test_unknown_pokemon_detail_mentions_name(self):
        response = client.get("/pokemon/mewtwo")
        body = response.json()
        assert "mewtwo" in body["detail"].lower() or "not found" in body["detail"].lower()


class TestPokemonResponseFormat:
    """Response is JSON with correct content-type."""

    def test_content_type_is_json(self):
        response = client.get("/pokemon/pikachu")
        assert "application/json" in response.headers["content-type"]


class TestExistingRoutesUnaffected:
    """Existing routes still work after router inclusion."""

    def test_home_still_works(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json()["status"] == "success"

    def test_items_still_works(self):
        response = client.get("/items")
        assert response.status_code == 200
        assert "items" in response.json()
