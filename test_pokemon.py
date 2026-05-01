"""Unit and integration tests for the /pokemon API endpoint."""

import pytest
from fastapi.testclient import TestClient

from main import app
from routers.pokemon import ALLOWED_POKEMON, get_pokemon

client = TestClient(app)


# ---------------------------------------------------------------------------
# Unit tests for the router module
# ---------------------------------------------------------------------------

class TestAllowedPokemonConstant:
    def test_allowed_set_contains_pikachu(self):
        assert "pikachu" in ALLOWED_POKEMON

    def test_allowed_set_contains_charlizad(self):
        assert "charlizad" in ALLOWED_POKEMON

    def test_allowed_set_contains_ash(self):
        assert "ash" in ALLOWED_POKEMON

    def test_allowed_set_has_exactly_three_entries(self):
        assert len(ALLOWED_POKEMON) == 3


# ---------------------------------------------------------------------------
# AC 1 – GET /pokemon/pikachu returns HTTP 200 with body {"name": "pikachu"}
# ---------------------------------------------------------------------------

class TestGetPikachuEndpoint:
    def test_status_200(self):
        response = client.get("/pokemon/pikachu")
        assert response.status_code == 200

    def test_body_contains_name_pikachu(self):
        response = client.get("/pokemon/pikachu")
        assert response.json() == {"name": "pikachu"}

    def test_case_insensitive_upper(self):
        response = client.get("/pokemon/PIKACHU")
        assert response.status_code == 200
        assert response.json()["name"] == "pikachu"

    def test_case_insensitive_mixed(self):
        response = client.get("/pokemon/Pikachu")
        assert response.status_code == 200
        assert response.json()["name"] == "pikachu"


# ---------------------------------------------------------------------------
# AC 2 – GET /pokemon/charlizad returns HTTP 200 with body {"name": "charlizad"}
# ---------------------------------------------------------------------------

class TestGetCharlizadEndpoint:
    def test_status_200(self):
        response = client.get("/pokemon/charlizad")
        assert response.status_code == 200

    def test_body_contains_name_charlizad(self):
        response = client.get("/pokemon/charlizad")
        assert response.json() == {"name": "charlizad"}

    def test_case_insensitive(self):
        response = client.get("/pokemon/CHARLIZAD")
        assert response.status_code == 200
        assert response.json()["name"] == "charlizad"


# ---------------------------------------------------------------------------
# AC 3 – GET /pokemon/ash returns HTTP 200 with body {"name": "ash"}
# ---------------------------------------------------------------------------

class TestGetAshEndpoint:
    def test_status_200(self):
        response = client.get("/pokemon/ash")
        assert response.status_code == 200

    def test_body_contains_name_ash(self):
        response = client.get("/pokemon/ash")
        assert response.json() == {"name": "ash"}

    def test_case_insensitive(self):
        response = client.get("/pokemon/ASH")
        assert response.status_code == 200
        assert response.json()["name"] == "ash"


# ---------------------------------------------------------------------------
# AC 4 – All three endpoints respond without server errors (no 5xx)
# ---------------------------------------------------------------------------

class TestNoServerErrors:
    @pytest.mark.parametrize("name", ["pikachu", "charlizad", "ash"])
    def test_no_5xx_for_allowed_names(self, name):
        response = client.get(f"/pokemon/{name}")
        assert response.status_code < 500

    def test_unknown_name_returns_404(self):
        response = client.get("/pokemon/bulbasaur")
        assert response.status_code == 404

    def test_unknown_name_error_detail(self):
        response = client.get("/pokemon/bulbasaur")
        data = response.json()
        assert "detail" in data

    def test_unknown_name_does_not_return_500(self):
        response = client.get("/pokemon/bulbasaur")
        assert response.status_code != 500


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:
    def test_empty_name_segment_not_matched(self):
        # /pokemon with no name → FastAPI returns 404 (no matching route)
        response = client.get("/pokemon")
        assert response.status_code in (404, 405, 307)

    def test_response_content_type_is_json(self):
        response = client.get("/pokemon/pikachu")
        assert "application/json" in response.headers["content-type"]

    def test_router_prefix_is_pokemon(self):
        """Ensure the router is mounted under /pokemon, not some other path."""
        response = client.get("/ash")
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# Regression – existing routes still work after router mount
# ---------------------------------------------------------------------------

class TestExistingRoutesUnaffected:
    def test_home_page_still_works(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_items_route_still_works(self):
        response = client.get("/items")
        assert response.status_code == 200
