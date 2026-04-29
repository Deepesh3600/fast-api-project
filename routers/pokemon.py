from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

# NOTE: "charlizad" is implemented verbatim per ticket spelling.
# Likely intended as "charizard" — confirm with reporter before merging.
VALID_POKEMON: set[str] = {"pikachu", "charlizad", "ash"}

router = APIRouter(prefix="/pokemon", tags=["pokemon"])


@router.get("/{name}", response_class=PlainTextResponse)
def get_pokemon(name: str) -> str:
    normalised = name.lower()
    if normalised not in VALID_POKEMON:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return normalised
