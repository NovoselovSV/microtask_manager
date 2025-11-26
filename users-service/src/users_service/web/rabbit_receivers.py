from faststream.rabbit.fastapi import RabbitMessage
from faststream_app import rabbit_router

from data.users_schemas import UserReadSchema

from services.sse_managers import sse_manager


@rabbit_router.subscriber('user.update')
async def handle_notification(user: UserReadSchema, msg: RabbitMessage):
    await sse_manager.broadcast(user.id, user)
