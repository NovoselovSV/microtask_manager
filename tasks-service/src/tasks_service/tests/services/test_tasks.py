from copy import copy
from datetime import datetime

import pytest
from pytest_lazy_fixtures import lf

from data.tasks import Task
from services.tasks import TaskService

FIRST_CALL_INDEX, FIRST_ARGUMENT_INDEX = (0, 0)


@pytest.mark.asyncio
async def test_is_task_belong_to_user_true_normal(
        test_first_task_first_user,
        prepare_tasks_is_task_belong_to_user_objects,
        mocker):
    fake_db = prepare_tasks_is_task_belong_to_user_objects()['fake_db']
    assert bool(await (TaskService(fake_db)
                       .is_task_belong_to_user(
        test_first_task_first_user.id,
        test_first_task_first_user.creator_id)))


@pytest.mark.asyncio
async def test_is_task_belong_to_user_false_normal(
        test_first_task_first_user,
        test_second_user_read_schema,
        prepare_tasks_is_task_belong_to_user_objects,
        mocker):
    prepared = prepare_tasks_is_task_belong_to_user_objects()
    fake_db, result_execute = prepared['fake_db'], prepared['result_execute']
    result_execute.scalar_one_or_none.return_value = None
    assert not bool(await (TaskService(fake_db)
                           .is_task_belong_to_user(
        test_first_task_first_user.id,
        test_second_user_read_schema.id)))


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'creator_schema', (
        (lf('test_user_read_schema'),
         lf('test_second_user_read_schema'))
    )
)
async def test_is_task_belong_to_user_db_query_mock(
        test_first_task_first_user,
        prepare_tasks_is_task_belong_to_user_objects,
        creator_schema,
        mocker):
    fake_db = prepare_tasks_is_task_belong_to_user_objects()['fake_db']
    creator_id = creator_schema.id
    await (TaskService(fake_db)
           .is_task_belong_to_user(
        test_first_task_first_user.id,
        creator_id))

    sql_query = str(fake_db.execute.call_args[
        FIRST_CALL_INDEX][
            FIRST_ARGUMENT_INDEX].compile(
            compile_kwargs={
                'literal_binds': True}))
    assert (f'{Task.__tablename__}.'
            f'{Task.id.property.columns[0].name} = '
            f'{test_first_task_first_user.id}' in sql_query)
    assert (f'{Task.__tablename__}.'
            f'{Task.creator_id.property.columns[0].name} = '
            f"'{creator_id.hex}'" in sql_query)


@pytest.mark.asyncio
async def test_get_by_id_normal(
        test_first_task_first_user,
        prepare_tasks_get_by_id_objects,
        mocker):
    prepared = prepare_tasks_get_by_id_objects()
    fake_db, result_execute = prepared['fake_db'], prepared['result_execute']
    result_execute.scalar_one_or_none.return_value = test_first_task_first_user
    assert (await (TaskService(fake_db)
                   .get_by_id(
        test_first_task_first_user.id
    )) == test_first_task_first_user)


@pytest.mark.asyncio
async def test_get_by_id_db_query_mock(
        test_first_task_first_user,
        prepare_tasks_get_by_id_objects,
        mocker):
    prepared = prepare_tasks_get_by_id_objects()
    fake_db = prepared['fake_db']
    await (TaskService(fake_db)
           .get_by_id(
        test_first_task_first_user.id
    ))
    sql_query = str(fake_db.execute.call_args[
        FIRST_CALL_INDEX][
            FIRST_ARGUMENT_INDEX].compile(
            compile_kwargs={
                'literal_binds': True}))
    assert (f'{Task.__tablename__}.'
            f'{Task.id.property.columns[0].name} = '
            f'{test_first_task_first_user.id}' in sql_query)


@pytest.mark.asyncio
async def test_get_all_for_normal(
        test_first_task_first_user,
        prepare_tasks_get_all_for_objects,
        mocker):
    fake_db = prepare_tasks_get_all_for_objects()['fake_db']
    assert (await (TaskService(fake_db)
                   .get_all_for(
        test_first_task_first_user.creator_id
    )))[0] == test_first_task_first_user


@pytest.mark.asyncio
async def test_get_all_for_db_query_mock(
        test_first_task_first_user,
        prepare_tasks_get_all_for_objects,
        mocker):
    fake_db = prepare_tasks_get_all_for_objects()['fake_db']
    assert (await (TaskService(fake_db)
                   .get_all_for(
        test_first_task_first_user.creator_id
    )))
    sql_query = str(fake_db.execute.call_args[
        FIRST_CALL_INDEX][
            FIRST_ARGUMENT_INDEX].compile(
            compile_kwargs={
                'literal_binds': True}))
    assert (f'{Task.__tablename__}.'
            f'{Task.creator_id.property.columns[0].name} = '
            f"'{test_first_task_first_user.creator_id.hex}'" in sql_query)


@pytest.mark.asyncio
async def test_create_normal(
        test_first_task_first_user,
        test_task_create_schema,
        prepare_tasks_create_objects,
        mocker):
    fake_db = prepare_tasks_create_objects()['fake_db']
    task = (await (TaskService(fake_db)
                   .create(
        test_task_create_schema,
        test_first_task_first_user.creator_id
    )))
    assert task
    assert task.description == test_task_create_schema.description
    assert task.creator_id == test_first_task_first_user.creator_id


@pytest.mark.asyncio
async def test_create_commited_data(
        test_first_task_first_user,
        test_task_create_schema,
        prepare_tasks_create_objects,
        mocker):
    fake_db = prepare_tasks_create_objects()['fake_db']
    await (TaskService(fake_db)
           .create(
        test_task_create_schema,
        test_first_task_first_user.creator_id
    ))
    fake_db.add.assert_called()
    fake_db.commit.assert_awaited()


@pytest.mark.asyncio
async def test_create_rabbit_sending(
        test_first_task_first_user,
        test_task_create_schema,
        prepare_tasks_create_objects,
        mocker):
    prepared = prepare_tasks_create_objects()
    fake_db, sending_mock = prepared['fake_db'], prepared['sending_mock']
    await (TaskService(fake_db)
           .create(
        test_task_create_schema,
        test_first_task_first_user.creator_id
    ))
    sending_mock.assert_awaited_once()
    new_task = sending_mock.call_args[FIRST_CALL_INDEX][FIRST_ARGUMENT_INDEX]
    assert new_task.creator_id == test_first_task_first_user.creator_id


@pytest.mark.asyncio
async def test_edit_normal(
        test_first_task_first_user,
        test_task_edit_schema,
        prepare_tasks_edit_objects,
        mocker):
    fake_db = prepare_tasks_edit_objects()['fake_db']
    assert (await (TaskService(fake_db)
                   .edit(
        test_first_task_first_user.id, test_task_edit_schema
    ))) == test_first_task_first_user


@pytest.mark.asyncio
async def test_edit_no_prev_state(
        test_first_task_first_user,
        test_task_edit_schema,
        prepare_tasks_edit_objects,
        mocker):
    prepared = prepare_tasks_edit_objects()
    fake_db, get_by_id_stab = prepared['fake_db'], prepared['get_by_id_stab']
    get_by_id_stab.return_value = None
    assert (await (TaskService(fake_db)
                   .edit(
        test_first_task_first_user.id, test_task_edit_schema
    ))) is None


@pytest.mark.asyncio
async def test_edit_db_query_mock(
        test_first_task_first_user,
        test_task_edit_schema,
        sql_value_formatter,
        prepare_tasks_edit_objects,
        mocker):
    fake_db = prepare_tasks_edit_objects()['fake_db']
    await (TaskService(fake_db)
           .edit(
        test_first_task_first_user.id, test_task_edit_schema
    ))
    sql_query = str(fake_db.execute.call_args[
        FIRST_CALL_INDEX][
            FIRST_ARGUMENT_INDEX].compile(
            compile_kwargs={
                'literal_binds': True}))
    updated_values = test_task_edit_schema.model_dump(exclude_unset=True)
    assert (f'{Task.__tablename__}.'
            f'{Task.id.property.columns[0].name} = '
            f'{test_first_task_first_user.id}' in sql_query)
    for name, value in updated_values.items():
        assert (f'{getattr(Task, name).property.columns[0].name}='
                f'{sql_value_formatter(value)}' in sql_query)


@pytest.mark.asyncio
async def test_edit_new_done_dt(
        test_first_task_first_user,
        test_task_edit_schema,
        sql_value_formatter,
        prepare_tasks_edit_objects,
        mocker):
    fake_db = prepare_tasks_edit_objects()['fake_db']
    test_task_edit_schema.done = True
    await (TaskService(fake_db)
           .edit(
        test_first_task_first_user.id, test_task_edit_schema
    ))
    sql_query = str(fake_db.execute.call_args[
        FIRST_CALL_INDEX][
            FIRST_ARGUMENT_INDEX].compile(
            compile_kwargs={
                'literal_binds': True}))
    assert (f'{Task.done_dt.property.columns[0].name}=' in sql_query)


@pytest.mark.asyncio
async def test_edit_new_final_dt_rabbit_send(
        test_first_task_first_user,
        test_task_edit_schema,
        sql_value_formatter,
        prepare_tasks_edit_objects,
        mocker):
    prepared = prepare_tasks_edit_objects()
    fake_db, send_task_mock, get_by_id_stab = prepared[
        'fake_db'], prepared['send_task_mock'], prepared['get_by_id_stab']
    another_final_dt_task = copy(test_first_task_first_user)
    another_final_dt_task.final_dt = datetime(2000, 1, 1, 12, 00)
    get_by_id_stab.side_effect = (
        test_first_task_first_user,
        another_final_dt_task)
    await (TaskService(fake_db)
           .edit(
        test_first_task_first_user.id, test_task_edit_schema
    ))
    send_task_mock.assert_awaited()


@pytest.mark.asyncio
async def test_edit_commited_data(
        test_first_task_first_user,
        test_task_edit_schema,
        sql_value_formatter,
        prepare_tasks_edit_objects,
        mocker):
    fake_db = prepare_tasks_edit_objects()['fake_db']
    await (TaskService(fake_db)
           .edit(
        test_first_task_first_user.id, test_task_edit_schema
    ))
    fake_db.commit.assert_awaited()
