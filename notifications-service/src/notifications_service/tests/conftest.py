import pytest_asyncio
import pytest
from faststream import TestApp
from faststream.rabbit import TestRabbitBroker

from faststream_app import faststream_app
from data.tasks_schemas import TaskSchema
from tests.constants import TASK_DATA, USER_ID, SECOND_USER_ID


@pytest_asyncio.fixture
async def test_app():
    async with TestRabbitBroker(faststream_app.broker):
        async with TestApp(faststream_app) as test_app:
            yield test_app


@pytest.fixture
def test_task_schema():
    return TaskSchema(**TASK_DATA)


@pytest.fixture
def test_user_id():
    return USER_ID


@pytest.fixture
def test_second_user_id():
    return SECOND_USER_ID
