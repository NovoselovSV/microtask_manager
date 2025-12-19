import pytest

from services.user_tasks_services import user_tasks_service


@pytest.fixture
def test_user_task_service():
    yield user_tasks_service
    user_tasks_service._connected_users.clear()
