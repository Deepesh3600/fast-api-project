from fastapi import APIRouter, Response

router = APIRouter(prefix="/pokemon", tags=["pokemon"])


@router.get("/pikachu", response_class=Response)
def get_pikachu() -> str:
    return Response(content="pikachu", media_type="text/plain")


@router.get("/charlizad", response_class=Response)
def get_charlizad() -> str:
    return Response(content="charlizad", media_type="text/plain")


@router.get("/ash", response_class=Response)
def get_ash() -> str:
    return Response(content="ash", media_type="text/plain")
