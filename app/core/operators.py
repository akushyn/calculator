import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class AbstractOperator(ABC):
    @abstractmethod
    async def _perform_operation(self, x: float, y: float) -> float:
        pass

    @property
    @abstractmethod
    def priority(self) -> int:
        pass

    async def perform(self, x: float, y: float) -> float:
        result = await self._perform_operation(x, y)
        logger.info(f"Perform {self.__class__.__name__}: {x}, {y}. Result={result}")
        return result


class AddOperator(AbstractOperator):
    async def _perform_operation(self, x: float, y: float) -> float:
        return x + y

    @property
    def priority(self) -> int:
        return 1


class SubOperator(AbstractOperator):
    async def _perform_operation(self, x: float, y: float) -> float:
        return x - y

    @property
    def priority(self) -> int:
        return 1


class MulOperator(AbstractOperator):
    async def _perform_operation(self, x: float, y: float) -> float:
        return x * y

    @property
    def priority(self) -> int:
        return 2


class DivOperator(AbstractOperator):
    async def _perform_operation(self, x: float, y: float) -> float:
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
