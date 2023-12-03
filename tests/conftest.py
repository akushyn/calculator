import pytest
from app.main import create_app
from starlette.testclient import TestClient


@pytest.fixture(autouse=True)
def app():
    app = create_app()
    return app


@pytest.fixture
def client(app):
    client = TestClient(app)
    return client
