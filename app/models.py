from pydantic import BaseModel


class CalculateRequest(BaseModel):
    expression: str
    colorize: bool = False


class CalculateResponse(BaseModel):
    result: float
    color: str | None = None
