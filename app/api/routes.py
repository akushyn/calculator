from fastapi import APIRouter

from app.core.operators import OPERATORS

router = APIRouter()


@router.get("/operators", response_model=list[str])
async def get_operators() -> list[str]:
    return list(OPERATORS.keys())
