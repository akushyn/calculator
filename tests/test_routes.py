import pytest

from app.core.operators import OPERATORS
from app.models import CalculateRequest


@pytest.fixture
def calculate_request():
    yield CalculateRequest(expression="2+3")


@pytest.mark.asyncio
async def test_get_operators(client):
    url = "/api/operators/"
    response = client.get(url)

    assert response.status_code == 200
    assert response.json() == list(OPERATORS.keys())


@pytest.mark.parametrize("colorize", [False, True])
@pytest.mark.asyncio
async def test_calculate(colorize, client, calculate_request):
    calculate_request.colorize = colorize
    response = client.post("/api/calculate/", json=calculate_request.model_dump())

    assert response.status_code == 200
    assert response.json() == {"result": 5.0, "color": None}
