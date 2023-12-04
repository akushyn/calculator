from abc import ABC, abstractmethod


class AbstractOperator(ABC):
    @abstractmethod
    async def perform(self, x: float, y: float) -> float:
        pass

    @property
    @abstractmethod
    def priority(self) -> int:
        pass


class AddOperator(AbstractOperator):
    async def perform(self, x: float, y: float) -> float:
        return x + y

    @property
    def priority(self) -> int:
        return 1


class SubOperator(AbstractOperator):
    async def perform(self, x: float, y: float) -> float:
        return x - y

    @property
    def priority(self) -> int:
        return 1


class MulOperator(AbstractOperator):
    async def perform(self, x: float, y: float) -> float:
        return x * y

    @property
    def priority(self) -> int:
        return 2


class DivOperator(AbstractOperator):
    async def perform(self, x: float, y: float) -> float:
        if y == 0:
            raise ValueError("Division by zero")

        return x / y

    @property
    def priority(self) -> int:
        return 2


OPERATORS = {
    "+": AddOperator,
    "-": SubOperator,
    "*": MulOperator,
    "/": DivOperator,
}


async def is_operator(op: str):
    return op in await get_operators_keys()


async def get_operator(op: str) -> AbstractOperator:
    if not await is_operator(op):
        raise NotImplementedError(
            f"Operator {op} does not support. Supported operators: "
            f"{await get_operators_keys()}"
        )
    return OPERATORS[op]()  # type: ignore


async def get_operators_keys() -> list[str]:
    return list(OPERATORS.keys())
