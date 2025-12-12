import pytest
from fastapi.testclient import TestClient
from fastapi_users.db import SQLAlchemyUserDatabase  # noqa F401
from starlette.routing import _DefaultLifespan

from data.users_schemas import UserReadSchema
from main import app
from services.sse_managers import sse_manager
from .constants import FIRST_USER_DATA, SECOND_USER_DATA


@pytest.fixture
def test_client():
    app.router.lifespan_context = _DefaultLifespan(app.router)
    with TestClient(app) as client:
        yield client


@pytest.fixture
def user_schema():
    return UserReadSchema(**FIRST_USER_DATA)


@pytest.fixture
def users_schemas():
    return (
        UserReadSchema(
            **FIRST_USER_DATA),
        UserReadSchema(
            **SECOND_USER_DATA))


@pytest.fixture
def test_sse_manager():
    yield sse_manager
    sse_manager._queues.clear()
