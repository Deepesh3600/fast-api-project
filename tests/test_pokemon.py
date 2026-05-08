"""Unit and integration tests for the /pokemon router (SCRUM-52)."""

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# ---------------------------------------------------------------------------
# Acceptance-criteria tests
# ---------------------------------------------------------------------------

class TestPokemonAC:
    """Each test maps directly to an acceptance criterion."""

    def test_ac1_pikachu_returns_pikachu(self):
        """AC1: Endpoint /pokemon/pikachu exists and returns 'pikachu'."""
        response = client.get("/pokemon/pikachu")
        assert response.status_code == 200
        assert response.json() == "pikachu"

    def test_ac2_charlizad_returns_charlizad(self):
        """AC2: Endpoint /pokemon/charlizad exists and returns 'charlizad'."""
        response = client.get("/pokemon/charlizad")
        assert response.status_code == 200
        assert response.json() == "charlizad"

    def test_ac3_ash_returns_ash(self):
        """AC3: Endpoint /pokemon/ash exists and returns 'ash'."""
        response = client.get("/pokemon/ash")
        assert response.status_code == 200
        assert response.json() == "ash"


# ---------------------------------------------------------------------------
# Edge-case / regression tests
# ---------------------------------------------------------------------------

class TestPokemonEdgeCases:
    def test_unknown_pokemon_returns_404(self):
        """Unknown sub-paths should yield 404."""
        response = client.get("/pokemon/bulbasaur")
        assert response.status_code == 404

    def test_root_pokemon_returns_404(self):
        """GET /pokemon with no sub-path should yield 404."""
        response = client.get("/pokemon")
        assert response.status_code == 404

    def test_post_pikachu_returns_405(self):
        """POST on a GET-only endpoint should yield 405."""
        response = client.post("/pokemon/pikachu")
        assert response.status_code == 405

    def test_post_charlizad_returns_405(self):
        response = client.post("/pokemon/charlizad")
        assert response.status_code == 405

    def test_post_ash_returns_405(self):
        response = client.post("/pokemon/ash")
        assert response.status_code == 405

    def test_case_sensitive_pikachu_upper(self):
        """Path matching should be case-sensitive; /Pikachu is not defined."""
        response = client.get("/pokemon/Pikachu")
        assert response.status_code == 404


# ---------------------------------------------------------------------------
# Existing-endpoint regression tests (no regressions from the new router)
# ---------------------------------------------------------------------------

class TestExistingEndpointsNotBroken:
    def test_home_page(self):
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "This is home page", "status": "success"}

    def test_get_all_items(self):
        response = client.get("/items")
        assert response.status_code == 200
        body = response.json()
        assert "items" in body
        assert "count" in body


# ---------------------------------------------------------------------------
# Router unit tests (test the router in isolation)
# ---------------------------------------------------------------------------

class TestPokemonRouterIsolated:
    """Instantiate the router on a minimal app to test it in isolation."""

    @pytest.fixture(autouse=True)
    def _isolated_client(self):
        from fastapi import FastAPI
        from routers.pokemon import router

        mini_app = FastAPI()
        mini_app.include_router(router)
        self.c = TestClient(mini_app)

    def test_isolated_pikachu(self):
        assert self.c.get("/pokemon/pikachu").json() == "pikachu"

    def test_isolated_charlizad(self):
        assert self.c.get("/pokemon/charlizad").json() == "charlizad"

    def test_isolated_ash(self):
        assert self.c.get("/pokemon/ash").json() == "ash"

    def test_router_prefix(self):
        from routers.pokemon import router
        assert router.prefix == "/pokemon"

    def test_router_tags(self):
        from routers.pokemon import router
        assert "pokemon" in router.tags
