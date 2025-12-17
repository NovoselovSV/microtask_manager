import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.routing import _DefaultLifespan

from configs.settings import Settings
from data.tasks import Task
from data.tasks_schemas import TaskCreateSchema, TaskEditSchema, TaskReadSchema
from data.users_schemas import UserReadSchema
from main import app
from p_database.db import get_db
from services.users import UserService
from tests.constants import (FIRST_TASK_FIRST_USER_DATA, FIRST_USER_DATA,
                             SECOND_USER_DATA)


@pytest.fixture
def test_client():
    app.router.lifespan_context = _DefaultLifespan(app.router)
    with TestClient(app) as client:
        yield client


@pytest.fixture
def test_task_read_schema():
    return TaskReadSchema(
        **FIRST_TASK_FIRST_USER_DATA)


@pytest.fixture
def test_task_create_schema():
    return TaskCreateSchema(
        **FIRST_TASK_FIRST_USER_DATA)


@pytest.fixture
def test_task_edit_schema():
    return TaskEditSchema(
        **FIRST_TASK_FIRST_USER_DATA)


@pytest.fixture
def test_user_read_schema():
    return UserReadSchema(
        **FIRST_USER_DATA)


@pytest.fixture
def sql_value_formatter():
    def format_value(value):
        if value is None:
            return 'null'
        elif isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            return f"'{value}'"
        else:
            return f"'{str(value)}'"
    return format_value


@pytest.fixture
def test_second_user_read_schema():
    return UserReadSchema(
        **SECOND_USER_DATA)


@pytest.fixture
def test_first_task_first_user():
    return Task(
        **FIRST_TASK_FIRST_USER_DATA)


@pytest.fixture
def settings():
    return Settings()


@pytest.fixture
def fake_db(mocker):
    mock_db = mocker.MagicMock(spec=AsyncSession)
    mock_db.execute = mocker.AsyncMock()
    return mock_db


@pytest.fixture
def fix_n_get_depends_get_current_user(mocker):
    mock_user_service = mocker.MagicMock(spec=UserService)
    mock_user_service.get_info = mocker.AsyncMock()
    mock_user_service.id = FIRST_USER_DATA['id']
    app.dependency_overrides[
        UserService.get_current_user] = lambda: mock_user_service

    yield mock_user_service

    app.dependency_overrides.clear()


@pytest.fixture
def fix_n_get_depends_get_user_info_before_logic(test_user_read_schema):
    app.dependency_overrides[
        UserService.get_user_info_before_logic] = lambda: test_user_read_schema
    yield test_user_read_schema

    app.dependency_overrides.clear()


@pytest.fixture
def fix_n_get_wrong_depends_get_user_info_before_logic(
        test_user_read_schema, mocker):
    mock_exception = mocker.MagicMock()
    mock_exception.side_effect = HTTPException(status.HTTP_401_UNAUTHORIZED)
    mock_exception.return_value = test_user_read_schema
    app.dependency_overrides[
        UserService.get_user_info_before_logic
    ] = lambda: mock_exception()

    yield test_user_read_schema

    app.dependency_overrides.clear()


@pytest.fixture
def fix_depends_get_db(mocker):
    mock_db_session = mocker.AsyncMock(spec=AsyncSession)
    app.dependency_overrides[get_db] = lambda: mock_db_session

    yield

    app.dependency_overrides.clear()
