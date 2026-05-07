import pytest
from fastapi.testclient import TestClient
from main import app
from routers.pokemon import VALID_POKEMON, get_pokemon

client = TestClient(app)


# --- Unit tests ---

class TestValidPokemonConstant:
    def test_contains_pikachu(self):
        assert "pikachu" in VALID_POKEMON

    def test_contains_charlizad(self):
        assert "charlizad" in VALID_POKEMON

    def test_contains_ash(self):
        assert "ash" in VALID_POKEMON

    def test_has_exactly_three_entries(self):
        assert len(VALID_POKEMON) == 3


# --- AC 1: GET /pokemon/pikachu → 200 "pikachu" (text/plain) ---

class TestPikachuEndpoint:
    def test_status_200(self):
        assert client.get("/pokemon/pikachu").status_code == 200

    def test_body_is_pikachu(self):
        assert client.get("/pokemon/pikachu").text == "pikachu"

    def test_content_type_plain_text(self):
        assert "text/plain" in client.get("/pokemon/pikachu").headers["content-type"]

    def test_case_insensitive_upper(self):
        r = client.get("/pokemon/PIKACHU")
        assert r.status_code == 200
        assert r.text == "pikachu"

    def test_case_insensitive_mixed(self):
        r = client.get("/pokemon/Pikachu")
        assert r.status_code == 200
        assert r.text == "pikachu"


# --- AC 2: GET /pokemon/charlizad → 200 "charlizad" (text/plain) ---

class TestCharlizadEndpoint:
    def test_status_200(self):
        assert client.get("/pokemon/charlizad").status_code == 200

    def test_body_is_charlizad(self):
        assert client.get("/pokemon/charlizad").text == "charlizad"

    def test_content_type_plain_text(self):
        assert "text/plain" in client.get("/pokemon/charlizad").headers["content-type"]

    def test_case_insensitive(self):
        r = client.get("/pokemon/CHARLIZAD")
        assert r.status_code == 200
        assert r.text == "charlizad"


# --- AC 3: GET /pokemon/ash → 200 "ash" (text/plain) ---

class TestAshEndpoint:
    def test_status_200(self):
        assert client.get("/pokemon/ash").status_code == 200

    def test_body_is_ash(self):
        assert client.get("/pokemon/ash").text == "ash"

    def test_content_type_plain_text(self):
        assert "text/plain" in client.get("/pokemon/ash").headers["content-type"]

    def test_case_insensitive(self):
        r = client.get("/pokemon/ASH")
        assert r.status_code == 200
        assert r.text == "ash"


# --- AC 4: No server errors (no 5xx) ---

class TestNoServerErrors:
    @pytest.mark.parametrize("name", ["pikachu", "charlizad", "ash"])
    def test_known_names_no_5xx(self, name):
        assert client.get(f"/pokemon/{name}").status_code < 500

    def test_unknown_returns_404(self):
        assert client.get("/pokemon/bulbasaur").status_code == 404

    def test_unknown_has_detail_key(self):
        body = client.get("/pokemon/bulbasaur").json()
        assert "detail" in body

    def test_unknown_does_not_return_500(self):
        assert client.get("/pokemon/bulbasaur").status_code != 500


# --- Edge cases ---

class TestEdgeCases:
    def test_bare_pokemon_path_not_200(self):
        r = client.get("/pokemon")
        assert r.status_code in (404, 405, 307)

    def test_router_mounted_under_pokemon_prefix(self):
        # /ash without prefix must 404 — router is mounted at /pokemon
        assert client.get("/ash").status_code == 404

    def test_post_method_not_allowed(self):
        assert client.post("/pokemon/pikachu").status_code == 405


# --- Regression: existing routes unaffected ---

class TestExistingRoutesUnaffected:
    def test_home_page_still_returns_200(self):
        r = client.get("/")
        assert r.status_code == 200
        assert r.json()["status"] == "success"

    def test_items_route_still_returns_200(self):
        r = client.get("/items")
        assert r.status_code == 200
        assert "items" in r.json()

    def test_get_item_by_id_still_works(self):
        r = client.get("/items/1")
        assert r.status_code == 200
        assert r.json()["status"] == "success"
