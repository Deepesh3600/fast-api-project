import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# --- Happy-path tests (acceptance criteria) ---


def test_get_pikachu():
    response = client.get("/pokemon/pikachu")
    assert response.status_code == 200
    assert response.json() == "pikachu"


def test_get_charlizard():
    response = client.get("/pokemon/charlizard")
    assert response.status_code == 200
    assert response.json() == "charlizard"


def test_get_ash():
    response = client.get("/pokemon/ash")
    assert response.status_code == 200
    assert response.json() == "ash"


# --- Edge-case tests ---


def test_pokemon_root_returns_404():
    """GET /pokemon (no sub-path) should 404 — no catch-all route defined."""
    response = client.get("/pokemon")
    assert response.status_code == 404


def test_unknown_pokemon_returns_404():
    """GET /pokemon/bulbasaur is not a defined route → 404."""
    response = client.get("/pokemon/bulbasaur")
    assert response.status_code == 404


def test_post_not_allowed():
    """POST to a pokemon endpoint should return 405 Method Not Allowed."""
    response = client.post("/pokemon/pikachu")
    assert response.status_code == 405


def test_trailing_slash_redirect_or_404():
    """Trailing slash on pokemon endpoints: FastAPI default redirects or 404."""
    response = client.get("/pokemon/pikachu/", follow_redirects=False)
    assert response.status_code in (200, 307, 404)
