from datetime import datetime, timedelta

import pytest

from tests.constants import TASK_END_QUEUE


def test_user_add_normal(test_user_task_service, test_user_id):
    prev_connected = test_user_task_service.is_user_connected(test_user_id)
    test_user_task_service.user_add(test_user_id)
    assert not prev_connected
    assert test_user_task_service.is_user_connected(test_user_id)


def test_user_add_duplicate(test_user_task_service, test_user_id):
    test_user_task_service.user_add(test_user_id)
    test_user_task_service.user_add(test_user_id)
    assert test_user_task_service.is_user_connected(test_user_id)


def test_user_remove_normal(test_user_task_service, test_user_id, mocker):
    mocker.patch('apscheduler.schedulers.asyncio.AsyncIOScheduler.remove_job')
    test_user_task_service.user_add(test_user_id)
    test_user_task_service.user_remove(test_user_id)
    assert not test_user_task_service.is_user_connected(test_user_id)


def test_user_remove_logic(test_user_task_service, test_user_id, mocker):
    remove_job_mock = mocker.patch(
        'apscheduler.schedulers.asyncio.AsyncIOScheduler.remove_job')
    test_user_task_service._connected_users[test_user_id] = ['something']
    test_user_task_service.user_remove(test_user_id)
    remove_job_mock.assert_called()


def test_user_remove_miss_user(test_user_task_service, test_user_id, mocker):
    mocker.patch('apscheduler.schedulers.asyncio.AsyncIOScheduler.remove_job')
    test_user_task_service.user_remove(test_user_id)
    assert not test_user_task_service.is_user_connected(test_user_id)


def test_is_user_connected_logic(test_user_task_service, test_user_id):
    base_state = test_user_task_service.is_user_connected(test_user_id)
    test_user_task_service.user_add(test_user_id)
    connected_state = test_user_task_service.is_user_connected(test_user_id)
    test_user_task_service.user_remove(test_user_id)
    disconnected_state = test_user_task_service.is_user_connected(test_user_id)
    assert not base_state
    assert connected_state
    assert not disconnected_state


def test_is_task_notifiable_normal(
        test_user_task_service,
        test_user_id,
        test_task_schema):
    test_user_task_service.user_add(test_user_id)
    test_task_schema.final_dt = datetime.now() + timedelta(days=1)
    assert test_user_task_service.is_task_notifiable(test_task_schema)


def test_is_task_notifiable_user_not_connected(
        test_user_task_service,
        test_user_id,
        test_task_schema):
    test_task_schema.final_dt = datetime.now() + timedelta(days=1)
    assert not test_user_task_service.is_task_notifiable(test_task_schema)


def test_is_task_notifiable_final_dt_before_now(
        test_user_task_service,
        test_user_id,
        test_task_schema):
    test_user_task_service.user_add(test_user_id)
    test_task_schema.final_dt = datetime.now() - timedelta(days=1)
    assert not test_user_task_service.is_task_notifiable(test_task_schema)


def test_user_task_add_normal(
        test_user_task_service,
        test_task_schema,
        mocker):
    mocker.patch(
        'services.user_tasks_services.UserTaskService.is_task_notifiable')
    mocker.patch('apscheduler.schedulers.asyncio.AsyncIOScheduler.add_job')
    test_user_task_service.user_add(test_task_schema.creator_id)
    test_user_task_service.user_task_add(test_task_schema)
    assert True


def test_user_task_add_not_notifiable(
        test_user_task_service,
        test_task_schema,
        mocker):
    is_task_notifiable_mock = mocker.patch(
        'services.user_tasks_services.UserTaskService.is_task_notifiable')
    is_task_notifiable_mock.return_value = False
    mocker.patch('apscheduler.schedulers.asyncio.AsyncIOScheduler.add_job')
    test_user_task_service.user_add(test_task_schema.creator_id)
    test_user_task_service.user_task_add(test_task_schema)
    assert True


def test_task_update_normal_logic(
        test_user_task_service,
        test_task_schema,
        mocker):
    mocker.patch(
        'services.user_tasks_services.UserTaskService.is_task_notifiable')
    add_job_mock = mocker.patch(
        'apscheduler.schedulers.asyncio.AsyncIOScheduler.add_job')
    remove_job_mock = mocker.patch(
        'apscheduler.schedulers.asyncio.AsyncIOScheduler.remove_job')
    mocker.patch('apscheduler.schedulers.asyncio.AsyncIOScheduler.get_job')
    test_user_task_service.task_update(test_task_schema)
    add_job_mock.assert_called()
    remove_job_mock.assert_called()


def test_task_update_hasnt_prev_task(
        test_user_task_service,
        test_task_schema,
        mocker):
    mocker.patch(
        'services.user_tasks_services.UserTaskService.is_task_notifiable')
    add_job_mock = mocker.patch(
        'apscheduler.schedulers.asyncio.AsyncIOScheduler.add_job')
    remove_job_mock = mocker.patch(
        'apscheduler.schedulers.asyncio.AsyncIOScheduler.remove_job')
    get_job_mock = mocker.patch(
        'apscheduler.schedulers.asyncio.AsyncIOScheduler.get_job')
    get_job_mock.return_value = None
    test_user_task_service.user_add(test_task_schema.creator_id)
    test_user_task_service.task_update(test_task_schema)
    add_job_mock.assert_called()
    remove_job_mock.assert_not_called()


def test_task_update_not_notifiable(
        test_user_task_service,
        test_task_schema,
        mocker):
    is_task_notifiable_mock = mocker.patch(
        'services.user_tasks_services.UserTaskService.is_task_notifiable')
    add_job_mock = mocker.patch(
        'apscheduler.schedulers.asyncio.AsyncIOScheduler.add_job')
    remove_job_mock = mocker.patch(
        'apscheduler.schedulers.asyncio.AsyncIOScheduler.remove_job')
    mocker.patch(
        'apscheduler.schedulers.asyncio.AsyncIOScheduler.get_job')
    is_task_notifiable_mock.return_value = False
    test_user_task_service.user_add(test_task_schema.creator_id)
    test_user_task_service.task_update(test_task_schema)
    add_job_mock.assert_not_called()
    remove_job_mock.assert_not_called()


@pytest.mark.asyncio
async def test_broadcast_finish_job(
        test_user_task_service,
        test_user_id,
        test_task_schema,
        mocker):
    publish_mock = mocker.patch('faststream.rabbit.RabbitBroker.publish')
    test_user_task_service._connected_users[test_task_schema.creator_id] = [
        str(test_task_schema.id)]
    await test_user_task_service.broadcast_finish_job(
        test_user_id, test_task_schema.id)
    publish_mock.assert_awaited_with(
        {'user_id': test_task_schema.creator_id,
         'task_id': test_task_schema.id},
        queue=TASK_END_QUEUE)
