import pytest

from tests.constants import BASE_API_VERSION, BASE_URL
from faststream_app import rabbit_router


@pytest.mark.parametrize(
    'url, method', (
        (f'/{BASE_API_VERSION}/sse', 'GET'),
        (f'/{BASE_API_VERSION}/auth/login', 'POST'),
        (f'/{BASE_API_VERSION}/auth/logout', 'POST'),
        (f'/{BASE_API_VERSION}/auth/register', 'POST'),
        (f'/{BASE_API_VERSION}/me', 'GET'),
        (f'/{BASE_API_VERSION}/me', 'PATCH'),
    )
)
def test_endpoints_existence(url, method, test_client):
    assert any([
        route.path == url and
        method in route.methods
        for route in test_client.app.routes
    ])


@pytest.mark.parametrize(
    'topic', (
        ('user.update',)
    )
)
def test_faststream_topics_existence(topic):
    assert any([
        subscriber.queue.name == topic
        for subscriber in rabbit_router.broker.subscribers
    ])


def test_root_path(test_client):
    assert test_client.app.root_path == '/api/users'
