from fastapi import APIRouter, HTTPException

ALLOWED_POKEMON: set[str] = {"pikachu", "charlizad", "ash"}

router = APIRouter(prefix="/pokemon", tags=["pokemon"])


@router.get("/{name}")
def get_pokemon(name: str) -> dict:
    """
    Get a Pokemon by name.

    Parameters:
        name: The Pokemon name (must be one of: pikachu, charlizad, ash)

    Returns:
        dict: {"name": <pokemon_name>} on success
    Raises:
        HTTPException 404: if name is not in the allow-list
    """
    normalised = name.lower()
    if normalised not in ALLOWED_POKEMON:
        raise HTTPException(status_code=404, detail=f"Pokemon '{name}' not found")
    return {"name": normalised}
