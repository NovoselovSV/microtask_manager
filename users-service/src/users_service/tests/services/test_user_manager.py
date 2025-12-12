from unittest.mock import MagicMock

import pytest

from data import User
from tests.constants import USER_UPDATE_QUEUE
from users_service.configs.auth import UserManager


@pytest.mark.asyncio
async def test_publish_rabbit_on_after_update(users_schemas, mocker):
    first_user, last_user = users_schemas
    mock_publish = mocker.patch('faststream_app.rabbit_router.broker.publish')
    user = User(**first_user.model_dump())
    await UserManager(MagicMock()).on_after_update(user, {'id': last_user.id})
    mock_publish.assert_awaited_once_with(
        first_user.model_dump(), queue=USER_UPDATE_QUEUE)
