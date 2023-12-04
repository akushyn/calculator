import pytest

from app.core.expression import ExpressionAnalyzer, Node, _clean, tokenize


@pytest.fixture
def expression():
    yield "2 + 3"


@pytest.fixture
def analyzer():
    yield ExpressionAnalyzer()


@pytest.mark.asyncio
async def test_build_tree(analyzer):
    tokens = ["2", "+", "3"]
    root = await analyzer.build_tree(tokens)

    assert isinstance(root, Node)
    assert root.value == "+"
    assert root.left_operand.value == "2"
    assert root.right_operand.value == "3"

    assert root.left_operand.left_operand is None
    assert root.left_operand.right_operand is None

    assert root.right_operand.left_operand is None
    assert root.right_operand.right_operand is None


@pytest.mark.asyncio
async def test_build_tree_with_no_tokens(analyzer):
    tokens = []
    root = await analyzer.build_tree(tokens)
    assert root is None


@pytest.mark.asyncio
async def test_evaluate_tree_none_root(analyzer):
    result = await analyzer.evaluate_tree(root=None)
    assert result == 0


@pytest.mark.asyncio
async def test_evaluate_tree(analyzer):
    left = Node(value="1")
    right = Node(value="2")

    root = Node(value="+")
    root.left_operand = left
    root.right_operand = right

    result = await analyzer.evaluate_tree(root)
    assert result == 3.0


@pytest.mark.parametrize(
    "expression, expected_result",
    [
        ("0+0", 0.0),
        ("2+3", 5.0),
        ("1-2+3", 2.0),
        ("1-2-3", -4.0),
        ("-1-2", -3.0),
        ("2+3*4", 14.0),
        ("2*3+4", 10.0),
        ("1 + 2 - 10 / 4 + 7 * 4", 28.5),
    ],
)
@pytest.mark.asyncio
async def test_calculate(analyzer, expression, expected_result):
    actual_result = await analyzer.calculate(expression)
    assert actual_result == expected_result


@pytest.mark.asyncio
async def test_tokenize(expression):
    tokens = await tokenize(expression)
    assert tokens == ["2", "+", "3"]


@pytest.mark.asyncio
async def test_clean(expression):
    clean_expression = await _clean(expression)
    assert clean_expression == "2+3"
