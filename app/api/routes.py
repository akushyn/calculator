from fastapi import APIRouter

from app.core.expression import ExpressionAnalyzer
from app.core.operators import get_operators_keys
from app.models import CalculateRequest, CalculateResponse

router = APIRouter()


async def process_calculation(request: CalculateRequest) -> CalculateResponse:
    analyzer = ExpressionAnalyzer()
    result = await analyzer.calculate(expression=request.expression)

    if request.colorize:
        color = await analyzer.get_colorizer().get_color(value=result)
        return CalculateResponse(
            result=result,
            color=color,
        )

    return CalculateResponse(result=result)


@router.get("/operators/", response_model=list[str])
async def operators() -> list[str]:
    return await get_operators_keys()


@router.post("/calculate/", response_model=CalculateResponse)
async def calculate(request: CalculateRequest) -> CalculateResponse:
    return await process_calculation(request)
