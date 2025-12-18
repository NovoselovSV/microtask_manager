import pytest
from services.rabbit_service import RabbitService
from data.tasks_schemas import TaskReadSchema


@pytest.mark.asyncio
async def test_publish(mocker):
    publish_mock = mocker.patch(
        'faststream_app.rabbit_router.broker.publish')
    test_data = {'test': 'data'}
    test_queue = 'test.queue'
    await RabbitService().publish(test_data, test_queue)
    publish_mock.assert_awaited_once_with(test_data, queue=test_queue)


@pytest.mark.asyncio
async def test_send_user_task(
        settings,
        test_first_task_first_user,
        prepare_rabbit_service_publish_objects):
    publish_mock = prepare_rabbit_service_publish_objects()['publish_mock']
    await RabbitService().send_user_task(test_first_task_first_user)
    publish_mock.assert_awaited_once_with(
        TaskReadSchema.model_validate(test_first_task_first_user).model_dump(),
        settings.task_user_queue)


@pytest.mark.asyncio
async def test_send_user_tasks(
        mocker,
        test_first_task_first_user,
):
    send_user_task_mock = mocker.patch(
        'services.rabbit_service.RabbitService.send_user_task')
    await RabbitService().send_user_tasks([test_first_task_first_user])
    send_user_task_mock.assert_awaited_once_with(
        test_first_task_first_user)


@pytest.mark.asyncio
async def test_send_user_connected(
        settings,
        test_user_read_schema,
        prepare_rabbit_service_publish_objects):
    publish_mock = prepare_rabbit_service_publish_objects()['publish_mock']
    id_str = str(test_user_read_schema.id)
    await RabbitService().send_user_connected(id_str)
    publish_mock.assert_awaited_once_with(
        id_str,
        settings.user_connected_queue)


@pytest.mark.asyncio
async def test_send_user_disconnected(
        settings,
        test_user_read_schema,
        prepare_rabbit_service_publish_objects):
    publish_mock = prepare_rabbit_service_publish_objects()['publish_mock']
    id_str = str(test_user_read_schema.id)
    await RabbitService().send_user_disconnected(id_str)
    publish_mock.assert_awaited_once_with(
        id_str,
        settings.user_disconnected_queue)


@pytest.mark.asyncio
async def test_send_task_update(
        settings,
        test_first_task_first_user,
        prepare_rabbit_service_publish_objects):
    publish_mock = prepare_rabbit_service_publish_objects()['publish_mock']
    await RabbitService().send_task_update(test_first_task_first_user)
    publish_mock.assert_awaited_once_with(
        TaskReadSchema.model_validate(test_first_task_first_user).model_dump(),
        settings.task_update_queue)
