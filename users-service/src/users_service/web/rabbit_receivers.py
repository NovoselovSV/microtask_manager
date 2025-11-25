from faststream_app import rabbit_broker

from users_service.data.users_schemas import UserReadSchema

from services.sse_managers import sse_manager


@rabbit_broker.subscriber('user.update')
async def handle_notification(user: UserReadSchema) -> None:
    await sse_manager.broadcast(user.id, user)
