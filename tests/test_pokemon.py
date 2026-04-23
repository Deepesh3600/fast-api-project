from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_pikachu_returns_200_and_name():
    r = client.get("/pokemon/pikachu")
    assert r.status_code == 200
    assert r.json() == "pikachu"


def test_charlizad_returns_200_and_name():
    r = client.get("/pokemon/charlizad")
    assert r.status_code == 200
    assert r.json() == "charlizad"


def test_ash_returns_200_and_name():
    r = client.get("/pokemon/ash")
    assert r.status_code == 200
    assert r.json() == "ash"


def test_unknown_pokemon_returns_404():
    r = client.get("/pokemon/bulbasaur")
    assert r.status_code == 404
    assert "not found" in r.json()["detail"].lower()


def test_case_sensitive_returns_404():
    r = client.get("/pokemon/Pikachu")
    assert r.status_code == 404


def test_bare_pokemon_path_returns_404():
    r = client.get("/pokemon")
    assert r.status_code in (404, 307)  # 307 if redirect_slashes fires; 404 if no route


def test_post_method_returns_405():
    r = client.post("/pokemon/pikachu")
    assert r.status_code == 405
