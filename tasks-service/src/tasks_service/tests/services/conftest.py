import jwt
import pytest

from services.sse_managers import sse_manager


@pytest.fixture
def valid_token(test_user_read_schema):
    secret = 'some_secret'
    id_str = str(test_user_read_schema.id)
    return {'token': jwt.encode({'sub': id_str}, secret),
            'id': id_str,
            'secret': secret}


@pytest.fixture
def valid_bearer_token(valid_token):
    return f'Bearer {valid_token["token"]}'


@pytest.fixture
def prepare_tasks_edit_objects(mocker, fake_db, test_first_task_first_user):
    def prepare_default():
        fake_db.commit = mocker.AsyncMock()
        send_task_mock = mocker.patch(
            'services.rabbit_service.RabbitService.send_task_update')
        get_by_id_stab = mocker.patch('services.tasks.TaskService.get_by_id')
        get_by_id_stab.return_value = test_first_task_first_user
        return {
            'fake_db': fake_db,
            'send_task_mock': send_task_mock,
            'get_by_id_stab': get_by_id_stab}
    return prepare_default


@pytest.fixture
def prepare_tasks_create_objects(mocker, fake_db):
    def prepare_default():
        fake_db.add = mocker.MagicMock()
        fake_db.commit = mocker.AsyncMock()
        sending_mock = mocker.patch(
            'services.rabbit_service.RabbitService.send_user_task')
        return {'fake_db': fake_db, 'sending_mock': sending_mock}
    return prepare_default


@pytest.fixture
def prepare_tasks_get_all_for_objects(
        mocker, fake_db, test_first_task_first_user):
    def prepare_default():
        result_execute = mocker.MagicMock()
        result_execute.scalars = mocker.MagicMock()
        return_scalars = mocker.MagicMock()
        return_scalars.all = mocker.MagicMock()
        return_scalars.all.return_value = [test_first_task_first_user]
        result_execute.scalars.return_value = return_scalars
        fake_db.execute.return_value = result_execute
        return {'fake_db': fake_db}
    return prepare_default


@pytest.fixture
def prepare_tasks_get_by_id_objects(
        mocker, fake_db):
    def prepare_default():
        result_execute = mocker.MagicMock()
        result_execute.scalar_one_or_none = mocker.MagicMock()
        fake_db.execute.return_value = result_execute
        return {'fake_db': fake_db, 'result_execute': result_execute}
    return prepare_default


@pytest.fixture
def prepare_tasks_is_task_belong_to_user_objects(
        mocker, fake_db, test_first_task_first_user):
    def prepare_default():
        result_execute = mocker.MagicMock()
        result_execute.scalar_one_or_none = mocker.MagicMock()
        result_execute.scalar_one_or_none.return_value = (
            test_first_task_first_user)
        fake_db.execute.return_value = result_execute
        return {'fake_db': fake_db, 'result_execute': result_execute}
    return prepare_default


@pytest.fixture
def test_sse_manager():
    yield sse_manager
    sse_manager._queues.clear()


@pytest.fixture
def prepare_sse_manager_subscribtion_objects(
        mocker, test_first_task_first_user):
    def prepare_default():
        send_user_connected_mock = mocker.patch(
            'services.rabbit_service.RabbitService.send_user_connected')
        send_user_tasks_mock = mocker.patch(
            'services.rabbit_service.RabbitService.send_user_tasks')
        get_db_mock = mocker.patch('p_database.db.get_db')
        get_all_for_mock = mocker.patch(
            'services.tasks.TaskService.get_all_for')
        return {
            'send_user_connected_mock': send_user_connected_mock,
            'send_user_tasks_mock': send_user_tasks_mock,
            'get_db_mock': get_db_mock,
            'get_all_for_mock': get_all_for_mock}
    return prepare_default


@pytest.fixture
def prepare_rabbit_service_publish_objects(mocker):
    def prepare_default():
        publish_mock = mocker.patch(
            'services.rabbit_service.RabbitService.publish')
        return {
            'publish_mock': publish_mock,
        }
    return prepare_default
