from fastapi import APIRouter

from app.core.operators import get_operators_keys

router = APIRouter()


@router.get("/operators", response_model=list[str])
async def operators() -> list[str]:
    return get_operators_keys()
