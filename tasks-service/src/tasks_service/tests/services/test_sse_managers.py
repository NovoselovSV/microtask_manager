import json
from asyncio.coroutines import inspect
from asyncio import Queue

import pytest


@pytest.mark.asyncio
async def test_get_subscription_queue(
        prepare_sse_manager_subscribtion_objects,
        test_sse_manager,
        test_user_read_schema,
        mocker):
    prepare_sse_manager_subscribtion_objects()
    queue = await test_sse_manager.subscribe(test_user_read_schema.id)
    assert hasattr(queue, 'get')
    assert inspect.iscoroutinefunction(queue.get)


@pytest.mark.asyncio
async def test_subscription_send_user_connected(
        prepare_sse_manager_subscribtion_objects,
        test_sse_manager,
        test_user_read_schema,
        mocker):
    send_user_connected_mock = prepare_sse_manager_subscribtion_objects()[
        'send_user_connected_mock']
    await test_sse_manager.subscribe(test_user_read_schema.id)
    send_user_connected_mock.assert_awaited_once_with(test_user_read_schema.id)


@pytest.mark.asyncio
async def test_subscription_send_user_tasks(
        prepare_sse_manager_subscribtion_objects,
        test_sse_manager,
        test_user_read_schema,
        test_first_task_first_user,
        mocker):
    prepared = prepare_sse_manager_subscribtion_objects()
    send_user_tasks_mock, get_all_for_mock = prepared[
        'send_user_tasks_mock'], prepared['get_all_for_mock']
    get_all_for_mock.return_value = [test_first_task_first_user]
    await test_sse_manager.subscribe(test_user_read_schema.id)
    send_user_tasks_mock.assert_awaited_once_with([test_first_task_first_user])


def test_get_multiple_subscription_queues(
        prepare_sse_manager_subscribtion_objects,
        test_sse_manager,
        test_user_read_schema,
        test_second_user_read_schema):
    prepare_sse_manager_subscribtion_objects()
    queue_first_user = test_sse_manager.subscribe(
        test_user_read_schema.id)
    queue_last_user = test_sse_manager.subscribe(
        test_second_user_read_schema.id)
    second_queue_first_user = test_sse_manager.subscribe(
        test_user_read_schema.id)
    assert queue_first_user != queue_last_user
    assert queue_first_user != second_queue_first_user
    assert second_queue_first_user != queue_last_user


@pytest.mark.asyncio
async def test_broadcast_normal(
        prepare_sse_manager_subscribtion_objects,
        test_sse_manager,
        test_user_read_schema,
        test_first_task_first_user):
    prepare_sse_manager_subscribtion_objects()
    queue = await test_sse_manager.subscribe(test_user_read_schema.id)
    await test_sse_manager.broadcast(test_user_read_schema.id,
                                     test_first_task_first_user.id)
    task_id = queue.get_nowait()
    assert task_id == json.dumps(test_first_task_first_user.id)


@pytest.mark.asyncio
async def test_the_only_user_broadcast(
        prepare_sse_manager_subscribtion_objects,
        test_sse_manager,
        test_user_read_schema,
        test_second_user_read_schema,
        test_first_task_first_user,
        mocker):
    prepare_sse_manager_subscribtion_objects()
    queue_first_user = await test_sse_manager.subscribe(
        test_user_read_schema.id)
    queue_last_user = await test_sse_manager.subscribe(
        test_second_user_read_schema.id)
    second_queue_first_user = await test_sse_manager.subscribe(
        test_user_read_schema.id)
    mocker.patch('services.sse_managers.SSEManager.unsubscribe')
    await test_sse_manager.broadcast(test_user_read_schema.id,
                                     test_first_task_first_user.id)
    assert queue_last_user.empty()
    assert queue_first_user.get_nowait() == json.dumps(
        test_first_task_first_user.id)
    assert second_queue_first_user.get_nowait(
    ) == json.dumps(test_first_task_first_user.id)


@pytest.mark.asyncio
async def test_unsubscribe_normal(
        prepare_sse_manager_subscribtion_objects,
        test_sse_manager,
        test_user_read_schema,
        test_first_task_first_user,
        mocker):
    prepare_sse_manager_subscribtion_objects()
    mocker.patch(
        'services.rabbit_service.RabbitService.send_user_disconnected')
    queue = await test_sse_manager.subscribe(test_user_read_schema.id)
    second_queue = await test_sse_manager.subscribe(test_user_read_schema.id)
    await test_sse_manager.unsubscribe(test_user_read_schema.id,
                                       queue)
    await test_sse_manager.broadcast(test_user_read_schema.id,
                                     test_first_task_first_user.id)
    assert queue.empty()
    assert not second_queue.empty()


@pytest.mark.asyncio
async def test_unsubscribe_wronq_queue(
        prepare_sse_manager_subscribtion_objects,
        test_sse_manager,
        test_user_read_schema,
        test_second_user_read_schema,
        test_first_task_first_user,
        mocker):
    prepare_sse_manager_subscribtion_objects()
    mocker.patch(
        'services.rabbit_service.RabbitService.send_user_disconnected')
    await test_sse_manager.subscribe(test_user_read_schema.id)
    second_user_queue = await test_sse_manager.subscribe(
        test_second_user_read_schema.id)
    await test_sse_manager.unsubscribe(test_user_read_schema.id,
                                       second_user_queue)
    assert True


@pytest.mark.asyncio
async def test_unsubscribe_send_user_disconnected(
        prepare_sse_manager_subscribtion_objects,
        test_sse_manager,
        test_user_read_schema,
        test_first_task_first_user,
        mocker):
    prepare_sse_manager_subscribtion_objects()
    send_user_disconnected_mock = mocker.patch(
        'services.rabbit_service.RabbitService.send_user_disconnected')
    queue = await test_sse_manager.subscribe(test_user_read_schema.id)
    await test_sse_manager.unsubscribe(test_user_read_schema.id,
                                       queue)
    send_user_disconnected_mock.assert_awaited()
