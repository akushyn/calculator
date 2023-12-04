from app.settings import settings


class ColorMixin:
    async def get_color(self, value: float) -> str | None:
        return None


class DefaultColorizer(ColorMixin):
    pass


class CalculateColorizer(DefaultColorizer):
    async def get_color(self, value: float) -> str | None:
        if value % 2 == 0:
            color = settings.calculate_even_color
        else:
            color = settings.calculate_odd_color
        return color
