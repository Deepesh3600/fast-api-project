from fastapi import APIRouter
from fastapi.responses import PlainTextResponse

router = APIRouter(prefix="/pokemon", tags=["pokemon"])

@router.get("/pikachu", response_class=PlainTextResponse)
def get_pikachu() -> str:
    """Returns the string 'pikachu'."""
    return "pikachu"

@router.get("/charlizad", response_class=PlainTextResponse)
def get_charlizad() -> str:
    """Returns the string 'charlizad'."""
    return "charlizad"

@router.get("/ash", response_class=PlainTextResponse)
def get_ash() -> str:
    """Returns the string 'ash'."""
    return "ash"
