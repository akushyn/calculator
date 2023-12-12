from fastapi import APIRouter, HTTPException

from app.core.colorizer import CalculateColorizer
from app.core.expression import ExpressionAnalyzer
from app.core.operators import get_operators_keys
from app.exceptions import CalculateException
from app.models import CalculateRequest, CalculateResponse

router = APIRouter()


async def get_analyzer(request: CalculateRequest):
    analyzer = ExpressionAnalyzer()
    if request.colorize:
        analyzer.colorizer = CalculateColorizer
    return analyzer


async def process_calculation(request: CalculateRequest) -> CalculateResponse:
    analyzer = await get_analyzer(request)
    try:
        result = await analyzer.calculate(expression=request.expression)
        color = await analyzer.get_color(result)
    except CalculateException as error:
        raise HTTPException(
            status_code=400, detail=f"Unprocessable operation: {str(error)}"
        ) from error

    return CalculateResponse(
        result=result,
        color=color,
    )


@router.get("/operators/", response_model=list[str])
async def operators() -> list[str]:
    return await get_operators_keys()


@router.post("/calculate/", response_model=CalculateResponse)
async def calculate(request: CalculateRequest) -> CalculateResponse:
    return await process_calculation(request)
