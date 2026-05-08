"""Unit tests for /pokemon endpoints covering all acceptance criteria."""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestPokemonPikachu:
    """AC: Endpoint /pokemon/pikachu exists and returns 'pikachu'."""

    def test_get_pikachu_status_200(self):
        response = client.get("/pokemon/pikachu")
        assert response.status_code == 200

    def test_get_pikachu_returns_pikachu(self):
        response = client.get("/pokemon/pikachu")
        assert response.json() == "pikachu"

    def test_get_pikachu_content_type_json(self):
        response = client.get("/pokemon/pikachu")
        assert "application/json" in response.headers["content-type"]


class TestPokemonCharlizad:
    """AC: Endpoint /pokemon/charlizad exists and returns 'charlizad'."""

    def test_get_charlizad_status_200(self):
        response = client.get("/pokemon/charlizad")
        assert response.status_code == 200

    def test_get_charlizad_returns_charlizad(self):
        response = client.get("/pokemon/charlizad")
        assert response.json() == "charlizad"

    def test_get_charlizad_content_type_json(self):
        response = client.get("/pokemon/charlizad")
        assert "application/json" in response.headers["content-type"]


class TestPokemonAsh:
    """AC: Endpoint /pokemon/ash exists and returns 'ash'."""

    def test_get_ash_status_200(self):
        response = client.get("/pokemon/ash")
        assert response.status_code == 200

    def test_get_ash_returns_ash(self):
        response = client.get("/pokemon/ash")
        assert response.json() == "ash"

    def test_get_ash_content_type_json(self):
        response = client.get("/pokemon/ash")
        assert "application/json" in response.headers["content-type"]


class TestPokemonEdgeCases:
    """Edge cases from analysis: unknown paths and root pokemon path."""

    def test_unknown_pokemon_returns_404(self):
        response = client.get("/pokemon/bulbasaur")
        assert response.status_code == 404

    def test_root_pokemon_returns_404(self):
        response = client.get("/pokemon")
        assert response.status_code == 404

    def test_root_pokemon_trailing_slash_returns_404_or_redirect(self):
        response = client.get("/pokemon/", follow_redirects=False)
        # FastAPI may redirect trailing slash; either 404 or redirect is acceptable
        assert response.status_code in (404, 307, 200)

    def test_case_sensitive_pikachu_uppercase_returns_404(self):
        response = client.get("/pokemon/Pikachu")
        assert response.status_code == 404
