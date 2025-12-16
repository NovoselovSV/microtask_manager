import pytest
from pytest_lazy_fixtures import lf
from services.tasks import TaskService
from data.tasks import Task

FIRST_CALL_INDEX, FIRST_ARGUMENT_INDEX = (0, 0)


@pytest.mark.asyncio
async def test_is_task_belong_to_user_true_normal(
        test_first_task_first_user,
        fake_db,
        mocker):
    result_execute = mocker.MagicMock()
    result_execute.scalar_one_or_none = mocker.MagicMock()
    result_execute.scalar_one_or_none.return_value = test_first_task_first_user
    fake_db.execute.return_value = result_execute
    assert bool(await (TaskService(fake_db)
                       .is_task_belong_to_user(
        test_first_task_first_user.id,
        test_first_task_first_user.creator_id)))


@pytest.mark.asyncio
async def test_is_task_belong_to_user_false_normal(
        test_first_task_first_user,
        test_second_user_read_schema,
        fake_db,
        mocker):
    result_execute = mocker.MagicMock()
    result_execute.scalar_one_or_none = mocker.MagicMock()
    result_execute.scalar_one_or_none.return_value = None
    fake_db.execute.return_value = result_execute
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
        fake_db,
        creator_schema,
        mocker):
    result_execute = mocker.MagicMock()
    result_execute.scalar_one_or_none = mocker.MagicMock()
    fake_db.execute.return_value = result_execute
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
        fake_db,
        mocker):
    result_execute = mocker.MagicMock()
    result_execute.scalar_one_or_none = mocker.MagicMock()
    result_execute.scalar_one_or_none.return_value = test_first_task_first_user
    fake_db.execute.return_value = result_execute
    assert (await (TaskService(fake_db)
                   .get_by_id(
        test_first_task_first_user.id
    )) == test_first_task_first_user)


@pytest.mark.asyncio
async def test_get_by_id_db_query_mock(
        test_first_task_first_user,
        fake_db,
        mocker):
    result_execute = mocker.MagicMock()
    result_execute.scalar_one_or_none = mocker.MagicMock()
    fake_db.execute.return_value = result_execute
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
        fake_db,
        mocker):
    result_execute = mocker.MagicMock()
    result_execute.scalars = mocker.MagicMock()
    return_scalars = mocker.MagicMock()
    return_scalars.all = mocker.MagicMock()
    return_scalars.all.return_value = [test_first_task_first_user]
    result_execute.scalars.return_value = return_scalars
    fake_db.execute.return_value = result_execute
    assert (await (TaskService(fake_db)
                   .get_all_for(
        test_first_task_first_user.creator_id
    )))[0] == test_first_task_first_user


@pytest.mark.asyncio
async def test_get_all_for_db_query_mock(
        test_first_task_first_user,
        fake_db,
        mocker):
    result_execute = mocker.MagicMock()
    result_execute.scalars = mocker.MagicMock()
    return_scalars = mocker.MagicMock()
    return_scalars.all = mocker.MagicMock()
    return_scalars.all.return_value = [test_first_task_first_user]
    result_execute.scalars.return_value = return_scalars
    fake_db.execute.return_value = result_execute
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
        fake_db,
        mocker):
    fake_db.add = mocker.MagicMock()
    fake_db.commit = mocker.AsyncMock()
    mocker.patch('services.rabbit_service.RabbitService.send_user_task')
    task = (await (TaskService(fake_db)
                   .create(
        test_task_create_schema,
        test_first_task_first_user.creator_id
    )))
    assert task
    assert task.description == test_task_create_schema.description
    assert task.creator_id == test_first_task_first_user.creator_id


@pytest.mark.asyncio
async def test_create_rabbit_sending(
        test_first_task_first_user,
        test_task_create_schema,
        fake_db,
        mocker):
    fake_db.add = mocker.MagicMock()
    fake_db.commit = mocker.AsyncMock()
    sending_mock = mocker.patch(
        'services.rabbit_service.RabbitService.send_user_task')
    await (TaskService(fake_db)
           .create(
        test_task_create_schema,
        test_first_task_first_user.creator_id
    ))
    sending_mock.assert_awaited_once()
    new_task = sending_mock.call_args[FIRST_CALL_INDEX][FIRST_ARGUMENT_INDEX]
    assert new_task.creator_id == test_first_task_first_user.creator_id
