from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/pokemon", tags=["pokemon"])

KNOWN_POKEMON: set[str] = {"pikachu", "charlizad", "ash"}


@router.get("/{name}")
def get_pokemon(name: str) -> dict:
    """
    Return the pokemon name if it is a known entry.

    Parameters:
        name: The pokemon name path segment (case-insensitive).

    Returns:
        dict: {"name": "<name>"} with HTTP 200.

    Raises:
        HTTPException 404: If the name is not in KNOWN_POKEMON.
    """
    normalised = name.lower()
    if normalised not in KNOWN_POKEMON:
        raise HTTPException(status_code=404, detail=f"Pokemon '{name}' not found")
    return {"name": normalised}
