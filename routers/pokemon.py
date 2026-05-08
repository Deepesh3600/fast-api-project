from fastapi import APIRouter

router = APIRouter(prefix="/pokemon", tags=["pokemon"])

_KNOWN_POKEMON = {"pikachu", "charlizard", "ash"}


@router.get("/pikachu")
def get_pikachu() -> str:
    """Returns the name 'pikachu'."""
    return "pikachu"


@router.get("/charlizard")
def get_charlizard() -> str:
    """Returns the name 'charlizard'."""
    return "charlizard"


@router.get("/ash")
def get_ash() -> str:
    """Returns the name 'ash'."""
    return "ash"
