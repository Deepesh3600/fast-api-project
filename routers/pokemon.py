from fastapi import APIRouter, HTTPException

router = APIRouter(tags=["pokemon"])


@router.get("/pikachu")
def get_pikachu() -> str:
    return "pikachu"


@router.get("/charlizad")
def get_charlizad() -> str:
    return "charlizad"


@router.get("/ash")
def get_ash() -> str:
    return "ash"


@router.get("/{name}")
def get_unknown_pokemon(name: str):
    raise HTTPException(status_code=404, detail=f"Pokemon '{name}' not found")
