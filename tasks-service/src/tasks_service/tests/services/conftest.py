import jwt
import pytest


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
