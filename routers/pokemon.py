from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

VALID_POKEMON: set[str] = {"pikachu", "charlizad", "ash"}

router = APIRouter(prefix="/pokemon", tags=["pokemon"])


@router.get("/{name}", response_class=PlainTextResponse)
def get_pokemon(name: str) -> str:
    """Return the Pokémon name as plain text, or 404 if unknown."""
    normalised = name.lower()
    if normalised not in VALID_POKEMON:
        raise HTTPException(status_code=404, detail=f"Pokemon '{name}' not found")
    return normalised
