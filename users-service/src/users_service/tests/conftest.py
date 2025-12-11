import pytest
from fastapi.testclient import TestClient
from starlette.routing import _DefaultLifespan

from main import app


@pytest.fixture
def test_client():
    app.router.lifespan_context = _DefaultLifespan(app.router)
    with TestClient(app) as client:
        yield client
