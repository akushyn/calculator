import pytest

from app.core.operators import (
    AddOperator,
    DivOperator,
    MulOperator,
    SubOperator,
    get_operator,
    get_operators_keys,
    is_operator,
)
from app.exceptions import CalculateException


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
    result = await operator._perform_operation(x, y)
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
    result = await operator._perform_operation(x, y)
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
@pytest.mark.asyncio
async def test_mul_operator(x, y, expected):
    operator = MulOperator()
    result = await operator._perform_operation(x, y)
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
@pytest.mark.asyncio
async def test_div_operator(x, y, expected):
    operator = DivOperator()
    result = await operator._perform_operation(x, y)
    assert result == expected


@pytest.mark.parametrize(
    "x, y",
    [
        (1, 0),
        (-1, 0),
        (0, 0),
    ],
)
@pytest.mark.asyncio
async def test_div_by_zero(x, y):
    operator = DivOperator()
    with pytest.raises(CalculateException) as exc_info:
        await operator._perform_operation(x, y)

    assert exc_info.type is CalculateException
    assert str(exc_info.value) == "Division by zero"


@pytest.mark.asyncio
async def test_get_operators_keys():
    keys = await get_operators_keys()
    assert keys == ["+", "-", "*", "/"]


@pytest.mark.parametrize(
    "op, expected",
    [
        ("+", True),
        ("-", True),
        ("*", True),
        ("/", True),
        (" ", False),
        ("1", False),
    ],
)
@pytest.mark.asyncio
async def test_is_operator(op, expected):
    result = await is_operator(op)
    assert result is expected


@pytest.mark.parametrize(
    "op, operator_class",
    [
        ("+", AddOperator),
        ("-", SubOperator),
        ("*", MulOperator),
        ("/", DivOperator),
    ],
)
@pytest.mark.asyncio
async def test_get_operator(op, operator_class):
    operator = await get_operator(op)
    assert isinstance(operator, operator_class)


@pytest.mark.asyncio
async def test_operator_not_implemented():
    not_implemented_operator = "^"
    with pytest.raises(NotImplementedError) as exc_info:
        await get_operator(not_implemented_operator)

    assert exc_info.type is NotImplementedError
    assert (
        str(exc_info.value)
        == "Operator ^ does not support. Supported operators: ['+', '-', '*', '/']"
    )
