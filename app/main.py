import logging.config

from fastapi import FastAPI

from app.api import routes
from app.settings import settings


def create_app():
    logging.config.dictConfig(settings.logging)

    app = FastAPI()
    app.include_router(router=routes.router, prefix="/api")

    return app


app = create_app()

