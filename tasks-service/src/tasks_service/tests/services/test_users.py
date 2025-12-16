import re

import pytest
from fastapi import HTTPException

from services.users import UserService


def test_get_user_id_from_token_normal(valid_token):
    bearer_token = f'Bearer {valid_token["token"]}'
    assert (UserService(bearer_token).id ==
            valid_token['id'])


@pytest.mark.parametrize(
    'token', (
        ('wrong_token', 'Bearer wrong_token')
    )
)
def test_get_user_id_from_token_exceptions(token):
    with pytest.raises(HTTPException):
        UserService(token)


@pytest.mark.asyncio
async def test_get_info_normal(
        httpx_mock,
        settings,
        test_user_read_schema,
        valid_bearer_token):
    httpx_mock.add_response(url=re.compile(
        fr'.*{settings.user_service.dsn}.*'),
        json=test_user_read_schema.model_dump(mode='json'))
    returning_user_schema = await UserService(valid_bearer_token).get_info()
    assert returning_user_schema == test_user_read_schema


@pytest.mark.asyncio
async def test_get_info_normal_authorization(
        httpx_mock,
        settings,
        test_user_read_schema,
        valid_bearer_token):
    httpx_mock.add_response(url=re.compile(
        fr'.*{settings.user_service.dsn}.*'),
        json=test_user_read_schema.model_dump(mode='json'))
    await UserService(valid_bearer_token).get_info()
    assert 'Authorization' in httpx_mock.get_request().headers
    assert httpx_mock.get_request(
    ).headers['Authorization'] == valid_bearer_token
