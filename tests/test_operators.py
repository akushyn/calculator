import pytest

from app.core.operators import AddOperator, SubOperator, MulOperator, DivOperator


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (0, 0, 0),
        (-1, -2, -3),
        (-1, 1, 0),
        (4, 5, 9),
        (6, 2, 8),
    ],
)
@pytest.mark.asyncio
async def test_add_operator(x, y, expected):
    operator = AddOperator()
    result = await operator.perform(x, y)
    assert result == expected


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (0, 0, 0),
        (-1, -2, 1),
        (-1, 1, -2),
        (4, 5, -1),
        (6, 2, 4),
    ],
)
@pytest.mark.asyncio
async def test_sub_operator(x, y, expected):
    operator = SubOperator()
    result = await operator.perform(x, y)
    assert result == expected


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (0, 0, 0),
        (-1, -2, 2),
        (-1, 1, -1),
        (4, 5, 20),
        (6, -2, -12),
    ],
)
async def test_mul_operator(x, y, expected):
    operator = MulOperator()
    result = await operator.perform(x, y)
    assert result == expected


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (-2, -1, 2),
        (-4, 1, -4),
        (20, 5, 4),
        (-1, 2, -0.5),
    ],
)
async def test_div_operator(x, y, expected):
    operator = DivOperator()
    result = await operator.perform(x, y)
    assert result == expected


@pytest.mark.parametrize(
    "x, y",
    [
        (1, 0),
        (-1, 0),
        (0, 0),
    ],
)
async def test_div_by_zero(x, y):
    operator = DivOperator()
    with pytest.raises(ValueError) as exc_info:
        await operator.perform(x, y)

    assert exc_info.type is ValueError
    assert str(exc_info.value) == "Division by zero"
