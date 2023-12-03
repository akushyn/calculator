from abc import ABC, abstractmethod


class AbstractOperator(ABC):
    @abstractmethod
    async def perform(self, x: float, y: float) -> float:
        pass


class AddOperator(AbstractOperator):
    async def perform(self, x: float, y: float) -> float:
        return x + y


class SubOperator(AbstractOperator):
    async def perform(self, x: float, y: float) -> float:
        return x - y


class MulOperator(AbstractOperator):
    async def perform(self, x: float, y: float) -> float:
        return x * y


class DivOperator(AbstractOperator):
    async def perform(self, x: float, y: float) -> float:
        if y == 0:
            raise ValueError("Division by zero")

        return x / y


OPERATORS = {
    "+": AddOperator,
    "-": SubOperator,
    "*": MulOperator,
    "/": DivOperator,
}
