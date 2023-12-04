import pytest
from starlette.testclient import TestClient

from app.main import create_app


@pytest.fixture(autouse=True)
def app():
    app = create_app()
    return app


@pytest.fixture
def client(app):
    client = TestClient(app)
    return client
