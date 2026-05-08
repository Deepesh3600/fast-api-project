from fastapi import APIRouter

router = APIRouter(prefix="/pokemon", tags=["pokemon"])


@router.get("/pikachu")
def get_pikachu() -> str:
    """Return the string 'pikachu'."""
    return "pikachu"


@router.get("/charlizad")
def get_charlizad() -> str:
    """Return the string 'charlizad'."""
    return "charlizad"


@router.get("/ash")
def get_ash() -> str:
    """Return the string 'ash'."""
    return "ash"
