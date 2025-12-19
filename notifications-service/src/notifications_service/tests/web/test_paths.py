import pytest

from tests import constants


@pytest.mark.parametrize('topic',
                         ((constants.USER_CONNECTED_QUEUE,
                           constants.USER_DISCONNECTED_QUEUE,
                           constants.TASK_USER_QUEUE,
                           constants.TASK_UPDATE_QUEUE)))
def test_faststream_topics_existence(topic, test_app):
    assert any([
        subscriber.queue.name == topic
        for subscriber in test_app.broker.subscribers
    ])
