"""Unit and integration tests for the /pokemon API endpoints."""
import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# AC-1: GET /pokemon/pikachu → 200 "pikachu"
# ---------------------------------------------------------------------------
def test_pikachu_status_200():
    response = client.get("/pokemon/pikachu")
    assert response.status_code == 200


def test_pikachu_body():
    response = client.get("/pokemon/pikachu")
    assert response.text == "pikachu"


def test_pikachu_content_type_plain_text():
    response = client.get("/pokemon/pikachu")
    assert "text/plain" in response.headers["content-type"]


# ---------------------------------------------------------------------------
# AC-2: GET /pokemon/charlizad → 200 "charlizad"
# ---------------------------------------------------------------------------
def test_charlizad_status_200():
    response = client.get("/pokemon/charlizad")
    assert response.status_code == 200


def test_charlizad_body():
    response = client.get("/pokemon/charlizad")
    assert response.text == "charlizad"


def test_charlizad_content_type_plain_text():
    response = client.get("/pokemon/charlizad")
    assert "text/plain" in response.headers["content-type"]


# ---------------------------------------------------------------------------
# AC-3: GET /pokemon/ash → 200 "ash"
# ---------------------------------------------------------------------------
def test_ash_status_200():
    response = client.get("/pokemon/ash")
    assert response.status_code == 200


def test_ash_body():
    response = client.get("/pokemon/ash")
    assert response.text == "ash"


def test_ash_content_type_plain_text():
    response = client.get("/pokemon/ash")
    assert "text/plain" in response.headers["content-type"]


# ---------------------------------------------------------------------------
# AC-4: /pokemon route group is registered and accessible
# ---------------------------------------------------------------------------
def test_pokemon_router_registered():
    """Verify that the /pokemon prefix is accessible (at least one route works)."""
    r1 = client.get("/pokemon/pikachu")
    r2 = client.get("/pokemon/charlizad")
    r3 = client.get("/pokemon/ash")
    assert all(r.status_code == 200 for r in [r1, r2, r3])


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------
def test_unknown_pokemon_returns_404():
    response = client.get("/pokemon/bulbasaur")
    assert response.status_code == 404


def test_pokemon_root_returns_404():
    response = client.get("/pokemon")
    assert response.status_code in (404, 405)


def test_post_pikachu_method_not_allowed():
    response = client.post("/pokemon/pikachu")
    assert response.status_code == 405


def test_post_charlizad_method_not_allowed():
    response = client.post("/pokemon/charlizad")
    assert response.status_code == 405


def test_post_ash_method_not_allowed():
    response = client.post("/pokemon/ash")
    assert response.status_code == 405


def test_pikachu_case_sensitive():
    """Routes should NOT match /pokemon/Pikachu (uppercase)."""
    response = client.get("/pokemon/Pikachu")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Router unit tests (isolated)
# ---------------------------------------------------------------------------
def test_get_pikachu_function():
    from routers.pokemon import get_pikachu
    assert get_pikachu() == "pikachu"


def test_get_charlizad_function():
    from routers.pokemon import get_charlizad
    assert get_charlizad() == "charlizad"


def test_get_ash_function():
    from routers.pokemon import get_ash
    assert get_ash() == "ash"


def test_router_prefix():
    from routers.pokemon import router
    assert router.prefix == "/pokemon"


def test_router_has_three_routes():
    from routers.pokemon import router
    assert len(router.routes) == 3
