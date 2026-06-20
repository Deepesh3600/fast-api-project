from fastapi import APIRouter

router = APIRouter(prefix="/pokemon", tags=["pokemon"])


@router.get("/pikachu")
def get_pikachu() -> str:
    return "pikachu"


@router.get("/charlizad")
def get_charlizad() -> str:
    return "charlizad"


@router.get("/ash")
def get_ash() -> str:
    return "ash"
