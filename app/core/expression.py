import logging
import re

from app.core.colorizer import DefaultColorizer
from app.core.operators import get_operator, get_operators_keys, is_operator

logger = logging.getLogger(__name__)


class Node:
    def __init__(self, value: str):
        self.value = value
        self.left_operand: Node | None = None
        self.right_operand: Node | None = None

    def __repr__(self):
        left = self.left_operand or ""
        right = self.right_operand or ""
        if left and right:
            return f"{left} --> {self.value} <-- {right}"
        elif left:
            return f"{left} --> {self.value}"
        elif right:
            return f"{self.value} <-- {right}"

        return self.value


class ExpressionAnalyzer:
    colorizer = DefaultColorizer

    def get_colorizer_class(self):
        return self.colorizer

    def get_colorizer(self):
        if not self.get_colorizer_class():
            return None
        return self.colorizer()

    async def build_tree(self, tokens) -> Node | None:
        logger.info(f"Build tree tokens: {tokens}")

        if not tokens:
            return None

        # find the operator with the lowest priority
        lowest_priority = float("inf")
        lowest_priority_idx = -1

        for i in range(len(tokens) - 1, -1, -1):
            token = tokens[i]

            if not await is_operator(op=token):
                continue

            # use operator priority property
            # to find the lowest priority and the lowest priority index
            operator = await get_operator(op=token)
            if operator.priority < lowest_priority:
                lowest_priority = operator.priority
                lowest_priority_idx = i

        # no operators found, assuming there is only a single number
        if lowest_priority_idx == -1:
            return Node(tokens[0])

        # recursively build left and right parts of tree nodes
        root = Node(tokens[lowest_priority_idx])
        root.left_operand = await self.build_tree(tokens[:lowest_priority_idx])
        root.right_operand = await self.build_tree(tokens[lowest_priority_idx + 1 :])

        return root

    async def evaluate_tree(self, root) -> float:
        logger.info(f"Evaluate tree: {root.__repr__()}")
        if root is None:
            return 0

        # reached leaves of the tree, it's always a number
        if _is_numeric(root.value):
            return float(root.value)

        left_val = await self.evaluate_tree(root.left_operand)
        right_val = await self.evaluate_tree(root.right_operand)

        # get appropriate operator and perform operation
        operator = await get_operator(op=root.value)
        return await operator.perform(x=left_val, y=right_val)

    async def calculate(self, expression: str):
        logger.info("Start calculate")
        tokens = await tokenize(expression)
        root = await self.build_tree(tokens)
        result = await self.evaluate_tree(root)

        logger.info("Done calculate")
        return result

    async def get_color(self, value: float) -> str | None:
        if not self.get_colorizer():
            return None
        return await self.get_colorizer().get_color(value)


async def _clean(expression: str) -> str:
    return expression.replace(" ", "")


def _is_numeric(s: str) -> bool:
    try:
        float(s)
        return True
    except ValueError:
        return False


async def tokenize(expression: str) -> list[str]:
    logger.info(f"Tokenize expression: {expression}")
    expression = await _clean(expression)
    operators = "|".join(re.escape(op) for op in await get_operators_keys())
    tokens = re.findall(r"\d*\.\d+|\d+|" + operators, expression)
    return tokens
