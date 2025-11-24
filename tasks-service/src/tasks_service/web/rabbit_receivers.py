from uuid import UUID
from faststream_app import rabbit_broker

from services.sse_managers import sse_manager


@rabbit_broker.subscriber('task-end')
async def handle_notification(user_id: UUID, task_id: int) -> None:
    await sse_manager.broadcast(user_id, task_id)
