from asyncio.coroutines import inspect
from asyncio import Queue

import pytest


def test_get_subscription_queue(test_sse_manager, user_schema):
    queue = test_sse_manager.subscribe(user_schema.id)
    assert hasattr(queue, 'get')
    assert inspect.iscoroutinefunction(queue.get)


def test_get_multiple_subscription_queues(test_sse_manager, users_schemas):
    first_user, last_user = users_schemas
    queue_first_user = test_sse_manager.subscribe(first_user.id)
    queue_last_user = test_sse_manager.subscribe(last_user.id)
    second_queue_first_user = test_sse_manager.subscribe(first_user.id)
    assert queue_first_user != queue_last_user
    assert queue_first_user != second_queue_first_user
    assert second_queue_first_user != queue_last_user


@pytest.mark.asyncio
async def test_broadcast(test_sse_manager, user_schema):
    queue = test_sse_manager.subscribe(user_schema.id)
    await test_sse_manager.broadcast(user_schema.id, user_schema)
    user_json = queue.get_nowait()
    assert user_json == user_schema.model_dump(mode='json')


@pytest.mark.asyncio
async def test_the_only_user_broadcast(test_sse_manager, users_schemas):
    first_user, last_user = users_schemas
    queue_first_user = test_sse_manager.subscribe(first_user.id)
    queue_last_user = test_sse_manager.subscribe(last_user.id)
    second_queue_first_user = test_sse_manager.subscribe(first_user.id)
    await test_sse_manager.broadcast(first_user.id, first_user)
    assert queue_last_user.empty()
    assert queue_first_user.get_nowait() == first_user.model_dump(mode='json')
    assert (second_queue_first_user.get_nowait() ==
            first_user.model_dump(mode='json'))


@pytest.mark.asyncio
async def test_unsubscribe_queue(test_sse_manager, user_schema):
    queue_first_user = test_sse_manager.subscribe(user_schema.id)
    second_queue_first_user = test_sse_manager.subscribe(user_schema.id)
    test_sse_manager.unsubscribe(user_schema.id, queue_first_user)
    await test_sse_manager.broadcast(user_schema.id, user_schema)
    assert queue_first_user.empty()
    assert (second_queue_first_user.get_nowait() ==
            user_schema.model_dump(mode='json'))


def test_unsubscribe_wrong_id(test_sse_manager, user_schema):
    queue_first_user = test_sse_manager.subscribe(user_schema.id)
    test_sse_manager.unsubscribe(user_schema.id, queue_first_user)
    test_sse_manager.unsubscribe(user_schema.id, queue_first_user)


@pytest.mark.asyncio
async def test_broadcast_wrong_id(test_sse_manager, user_schema):
    await test_sse_manager.broadcast(user_schema.id, user_schema)
