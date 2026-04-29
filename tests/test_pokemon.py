import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture
def client():
    return TestClient(app)


def test_pikachu_returns_200_and_body(client):
    r = client.get("/pokemon/pikachu")
    assert r.status_code == 200
    assert r.text == "pikachu"


def test_charlizad_returns_200_and_body(client):
    r = client.get("/pokemon/charlizad")
    assert r.status_code == 200
    assert r.text == "charlizad"


def test_ash_returns_200_and_body(client):
    r = client.get("/pokemon/ash")
    assert r.status_code == 200
    assert r.text == "ash"


def test_content_type_is_text_plain(client):
    for name in ("pikachu", "charlizad", "ash"):
        r = client.get(f"/pokemon/{name}")
        assert "text/plain" in r.headers["content-type"]


def test_unknown_pokemon_returns_404(client):
    r = client.get("/pokemon/bulbasaur")
    assert r.status_code == 404


def test_no_subpath_returns_404(client):
    # /pokemon with no name segment — FastAPI returns 404/422 automatically
    r = client.get("/pokemon/")
    assert r.status_code in (404, 422)


def test_case_insensitive_pikachu(client):
    r = client.get("/pokemon/Pikachu")
    assert r.status_code == 200
    assert r.text == "pikachu"


def test_non_get_method_returns_405(client):
    r = client.post("/pokemon/pikachu")
    assert r.status_code == 405
