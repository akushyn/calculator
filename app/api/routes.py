from fastapi import APIRouter

from app.core.expression import ExpressionAnalyzer
from app.core.operators import get_operators_keys
from app.models import CalculateRequest, CalculateResponse, ColorizeCalculateResponse

router = APIRouter()


async def process_calculation(
    request: CalculateRequest,
) -> ColorizeCalculateResponse | CalculateResponse:
    analyzer = ExpressionAnalyzer()
    result = await analyzer.calculate(expression=request.expression)

    if request.colorize:
        color = await analyzer.get_colorizer().get_color(value=result)
        return ColorizeCalculateResponse(
            result=result,
            color=color,
        )

    return CalculateResponse(result=result)


@router.get("/operators/", response_model=list[str])
async def operators() -> list[str]:
    return await get_operators_keys()


@router.post(
    "/calculate/", response_model=CalculateResponse | ColorizeCalculateResponse
)
async def calculate(
    request: CalculateRequest,
) -> CalculateResponse | ColorizeCalculateResponse:
    return await process_calculation(request)
