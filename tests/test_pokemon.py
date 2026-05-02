from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_pikachu():
    response = client.get("/pokemon/pikachu")
    assert response.status_code == 200
    assert response.json() == "pikachu"


def test_get_charlizad():
    response = client.get("/pokemon/charlizad")
    assert response.status_code == 200
    assert response.json() == "charlizad"


def test_get_ash():
    response = client.get("/pokemon/ash")
    assert response.status_code == 200
    assert response.json() == "ash"


def test_unknown_pokemon_returns_404():
    response = client.get("/pokemon/bulbasaur")
    assert response.status_code == 404


def test_base_pokemon_route_returns_404():
    response = client.get("/pokemon")
    assert response.status_code == 404
