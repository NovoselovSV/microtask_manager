import pytest
from fastapi import HTTPException, status

from tests.constants import BASE_API_VERSION


def test_get_tasks_normal(
        test_client,
        fix_n_get_depends_get_current_user,
        fix_depends_get_db,
        test_task_read_schema,
        mocker):
    all_tasks_mock = mocker.patch('services.tasks.TaskService.get_all_for')
    all_tasks_mock.return_value = [
        test_task_read_schema]
    response = test_client.get(f'/{BASE_API_VERSION}')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [test_task_read_schema.model_dump(mode='json')]


def test_get_tasks_wrong_user(
        test_client,
        fix_n_get_depends_get_current_user,
        fix_depends_get_db,
        test_task_read_schema,
        mocker):
    all_tasks_mock = mocker.patch('services.tasks.TaskService.get_all_for')
    all_tasks_mock.return_value = [
        test_task_read_schema]
    (fix_n_get_depends_get_current_user
     .get_info.side_effect) = HTTPException(status.HTTP_401_UNAUTHORIZED)
    response = test_client.get(f'/{BASE_API_VERSION}')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.parametrize(
    'token', (
        ('Bearer wrong_token',
         'wrong_token')
    )
)
def test_get_tasks_wrong_token(
        test_client,
        fix_depends_get_db,
        test_task_read_schema,
        token):
    response = test_client.get(
        f'/{BASE_API_VERSION}',
        headers={'Authorization': token})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_create_tasks_normal(
        test_client,
        fix_n_get_depends_get_user_info_before_logic,
        fix_depends_get_db,
        test_task_read_schema,
        test_task_create_schema,
        mocker):
    create_task_mock = mocker.patch('services.tasks.TaskService.create')
    create_task_mock.return_value = test_task_read_schema
    response = test_client.post(
        f'/{BASE_API_VERSION}',
        json=test_task_create_schema.model_dump(mode='json'))
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json() == test_task_read_schema.model_dump(mode='json')


def test_create_tasks_wrong_data(
        test_client,
        fix_n_get_depends_get_user_info_before_logic,
        fix_depends_get_db,
        test_task_read_schema,
        mocker):
    create_task_mock = mocker.patch('services.tasks.TaskService.create')
    create_task_mock.return_value = test_task_read_schema
    response = test_client.post(
        f'/{BASE_API_VERSION}',
        json={'wrong': 'data'})
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT


def test_create_task_wrong_user(
        test_client,
        fix_depends_get_db,
        fix_n_get_wrong_depends_get_user_info_before_logic,
        test_task_read_schema,
        test_user_read_schema,
        test_task_create_schema
):
    response = test_client.post(
        f'/{BASE_API_VERSION}',
        json=test_task_create_schema.model_dump(mode='json'))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_edit_task_normal(
        test_client,
        fix_n_get_depends_get_user_info_before_logic,
        fix_depends_get_db,
        test_task_read_schema,
        test_task_edit_schema,
        mocker):
    is_task_belong_to_user_mock = mocker.patch(
        'services.tasks.TaskService.is_task_belong_to_user')
    is_task_belong_to_user_mock.return_value = True
    edit_task_mock = mocker.patch('services.tasks.TaskService.edit')
    edit_task_mock.return_value = test_task_read_schema
    response = test_client.patch(
        f'/{BASE_API_VERSION}/{test_task_read_schema.id}',
        json=test_task_edit_schema.model_dump(mode='json'))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == test_task_read_schema.model_dump(mode='json')


def test_edit_task_wrong_user(
        test_client,
        fix_depends_get_db,
        fix_n_get_wrong_depends_get_user_info_before_logic,
        test_task_read_schema,
        test_user_read_schema,
        test_task_edit_schema,
):
    response = test_client.patch(
        f'/{BASE_API_VERSION}/{test_task_read_schema.id}',
        json=test_task_edit_schema.model_dump(mode='json'))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_edit_task_is_not_belong(
        test_client,
        fix_n_get_depends_get_user_info_before_logic,
        fix_depends_get_db,
        test_task_read_schema,
        test_task_edit_schema,
        mocker):
    is_task_belong_to_user_mock = mocker.patch(
        'services.tasks.TaskService.is_task_belong_to_user')
    is_task_belong_to_user_mock.return_value = False
    edit_task_mock = mocker.patch('services.tasks.TaskService.edit')
    edit_task_mock.return_value = test_task_read_schema
    response = test_client.patch(
        f'/{BASE_API_VERSION}/{test_task_read_schema.id}',
        json=test_task_edit_schema.model_dump(mode='json'))
    assert response.status_code == status.HTTP_404_NOT_FOUND
