"""
Unit and integration tests for main.py — covers all acceptance criteria for
the /pokemon endpoint feature (SCRUM-1).

Acceptance Criteria (from analysis.json):
  AC1: GET /pokemon returns HTTP 200 with a valid Pokemon payload.
  AC2: Response body contains Pokemon objects with identifiable fields (name/id).
  AC3: Endpoint is accessible via the existing API routing infrastructure.
  AC4: Response is serialized as JSON consistent with other API endpoints.
  AC5: Endpoint integrates cleanly without breaking existing routes or services.
"""

import pytest
from fastapi.testclient import TestClient

from main import app, pokemon_db, items_db, Pokemon

client = TestClient(app)


# ---------------------------------------------------------------------------
# AC1 — GET /pokemon returns HTTP 200
# ---------------------------------------------------------------------------

class TestGetAllPokemonStatus:
    def test_returns_200(self):
        response = client.get("/pokemon")
        assert response.status_code == 200

    def test_content_type_is_json(self):
        response = client.get("/pokemon")
        assert "application/json" in response.headers["content-type"]


# ---------------------------------------------------------------------------
# AC2 — Response body contains Pokemon objects with identifiable fields
# ---------------------------------------------------------------------------

class TestGetAllPokemonPayload:
    def test_response_has_pokemon_key(self):
        response = client.get("/pokemon")
        body = response.json()
        assert "pokemon" in body

    def test_response_has_count_key(self):
        response = client.get("/pokemon")
        body = response.json()
        assert "count" in body
        assert body["count"] == len(pokemon_db)

    def test_each_pokemon_has_id(self):
        response = client.get("/pokemon")
        for pokemon in response.json()["pokemon"]:
            assert "id" in pokemon

    def test_each_pokemon_has_name(self):
        response = client.get("/pokemon")
        for pokemon in response.json()["pokemon"]:
            assert "name" in pokemon
            assert isinstance(pokemon["name"], str)
            assert len(pokemon["name"]) > 0

    def test_each_pokemon_has_type(self):
        response = client.get("/pokemon")
        for pokemon in response.json()["pokemon"]:
            assert "type" in pokemon

    def test_seed_data_bulbasaur_present(self):
        response = client.get("/pokemon")
        names = [p["name"] for p in response.json()["pokemon"]]
        assert "Bulbasaur" in names

    def test_seed_data_charmander_present(self):
        response = client.get("/pokemon")
        names = [p["name"] for p in response.json()["pokemon"]]
        assert "Charmander" in names

    def test_seed_data_squirtle_present(self):
        response = client.get("/pokemon")
        names = [p["name"] for p in response.json()["pokemon"]]
        assert "Squirtle" in names


# ---------------------------------------------------------------------------
# AC3 — Accessible via existing routing infrastructure
# ---------------------------------------------------------------------------

class TestGetPokemonById:
    def test_returns_200_for_existing_pokemon(self):
        response = client.get("/pokemon/1")
        assert response.status_code == 200

    def test_returns_success_status_for_existing_pokemon(self):
        response = client.get("/pokemon/1")
        body = response.json()
        assert body["status"] == "success"

    def test_response_has_data_key(self):
        response = client.get("/pokemon/1")
        assert "data" in response.json()

    def test_pokemon_id_matches_requested(self):
        response = client.get("/pokemon/2")
        assert response.json()["data"]["id"] == 2

    def test_missing_pokemon_returns_error_json(self):
        response = client.get("/pokemon/99")
        body = response.json()
        assert body["status"] == "error"
        assert "error" in body

    def test_missing_pokemon_still_returns_200(self):
        """Matches existing get_item not-found convention (200 + error JSON)."""
        response = client.get("/pokemon/99")
        assert response.status_code == 200


# ---------------------------------------------------------------------------
# AC4 — JSON format consistent with other endpoints
# ---------------------------------------------------------------------------

class TestResponseFormatConsistency:
    def test_pokemon_list_mirrors_items_structure(self):
        """GET /pokemon should mirror GET /items structure."""
        items_resp = client.get("/items")
        pokemon_resp = client.get("/pokemon")
        items_body = items_resp.json()
        pokemon_body = pokemon_resp.json()
        # Both should have a collection key and a count key
        assert "items" in items_body and "count" in items_body
        assert "pokemon" in pokemon_body and "count" in pokemon_body

    def test_pokemon_by_id_mirrors_item_by_id_structure(self):
        """GET /pokemon/{id} should mirror GET /items/{id} structure."""
        item_resp = client.get("/items/1")
        pokemon_resp = client.get("/pokemon/1")
        assert set(item_resp.json().keys()) == set(pokemon_resp.json().keys())

    def test_pokemon_not_found_mirrors_item_not_found_structure(self):
        item_resp = client.get("/items/999")
        pokemon_resp = client.get("/pokemon/999")
        assert set(item_resp.json().keys()) == set(pokemon_resp.json().keys())


# ---------------------------------------------------------------------------
# AC5 — Existing routes unaffected
# ---------------------------------------------------------------------------

class TestExistingRoutesUnaffected:
    def test_home_returns_200(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_home_returns_message(self):
        assert "message" in client.get("/").json()

    def test_items_returns_200(self):
        response = client.get("/items")
        assert response.status_code == 200

    def test_items_payload_intact(self):
        body = client.get("/items").json()
        assert "items" in body
        assert body["count"] == len(items_db)

    def test_item_by_id_returns_200(self):
        assert client.get("/items/1").status_code == 200

    def test_create_item_still_works(self):
        payload = {"id": 999, "name": "Test", "description": "d", "price": 1.0}
        response = client.post("/items", json=payload)
        assert response.status_code == 200
        assert response.json()["status"] == "success"


# ---------------------------------------------------------------------------
# Pokemon Pydantic model unit tests
# ---------------------------------------------------------------------------

class TestPokemonModel:
    def test_valid_pokemon_model(self):
        p = Pokemon(id=1, name="Pikachu", type="Electric")
        assert p.id == 1
        assert p.name == "Pikachu"
        assert p.type == "Electric"
        assert p.description is None  # optional field

    def test_pokemon_model_with_description(self):
        p = Pokemon(id=4, name="Mewtwo", type="Psychic", description="Genetically engineered.")
        assert p.description == "Genetically engineered."

    def test_pokemon_model_requires_id(self):
        with pytest.raises(Exception):
            Pokemon(name="Pikachu", type="Electric")

    def test_pokemon_model_requires_name(self):
        with pytest.raises(Exception):
            Pokemon(id=1, type="Electric")

    def test_pokemon_model_requires_type(self):
        with pytest.raises(Exception):
            Pokemon(id=1, name="Pikachu")
