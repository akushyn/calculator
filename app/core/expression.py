import re

from app.core.operators import get_operators_keys, get_operator, is_operator


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
    async def build_tree(self, tokens) -> Node | None:
        if not tokens:
            return None

        # find the operator with the lowest priority
        lowest_priority = float("inf")
        lowest_priority_idx = -1

        for i in range(len(tokens) - 1, -1, -1):
            token = tokens[i]

            if not await is_operator(op=token):
                continue

            # use operator priority property to find the lowest priority and the lowest priority index
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
        if root is None:
            return 0

        # reached leaves of the tree, it's always a number
        if root.value.isdigit():
            return float(root.value)

        left_val = await self.evaluate_tree(root.left_operand)
        right_val = await self.evaluate_tree(root.right_operand)

        # get appropriate operator and perform operation
        operator = await get_operator(op=root.value)
        return await operator.perform(x=left_val, y=right_val)

    async def calculate(self, expression: str):
        tokens = await tokenize(expression)
        root = await self.build_tree(tokens)
        result = await self.evaluate_tree(root)

        return result


async def _clean(expression: str) -> str:
    return expression.replace(" ", "")


async def tokenize(expression: str) -> list[str]:
    expression = await _clean(expression)
    operators = "|".join(re.escape(op) for op in await get_operators_keys())
    tokens = re.findall(r"\d+|" + operators, expression)
    return tokens
