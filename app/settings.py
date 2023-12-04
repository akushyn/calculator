import os

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    calculate_even_color: str = "green"
    calculate_odd_color: str = "red"

    logging_handlers: list[str] = ["console"]
    logging_level: str = "DEBUG"

    model_config = SettingsConfigDict(
        case_sensitive=False,
        # Usage of .env file may be disabled by NO_DOT_ENV environment
        # variable to avoid confusions and errors with double reading and
        # extra variables when using Docker Compose or any other upper layer
        # that reads .env file.
        env_file=".env" if not os.getenv("NO_DOT_ENV", "") else None,
        env_file_encoding="utf-8",
    )

    @computed_field  # type: ignore[misc]
    @property
    def logging(self) -> dict:
        return {
            "version": 1,
            "disable_existing_loggers": True,
            "formatters": {
                "file": {
                    "format": "[%(asctime)s: %(levelname)s/%(name)s] %(message)s",
                },
            },
            "handlers": {
                "console": {
                    "level": self.logging_level,
                    "class": "logging.StreamHandler",
                    "formatter": "file",
                },
            },
            "loggers": {
                "uvicorn": {
                    "level": "INFO",
                    "handlers": self.logging_handlers,
                    "propagate": True,
                },
                "app": {
                    "level": "DEBUG",
                    "handlers": self.logging_handlers,
                    "propagate": True,
                },
            },
        }


def _parse_csv(value: str) -> list[str]:
    return [chunk.strip() for chunk in value.split(",")]


settings = Settings()
