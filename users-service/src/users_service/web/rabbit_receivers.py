from faststream_app import rabbit_broker

from users_service.data.users_schemas import UserRead

from .sse_managers import sse_manager


@rabbit_broker.subscriber('update-user')
async def handle_notification(user: UserRead) -> None:
    await sse_manager.broadcast(user.id, user)
