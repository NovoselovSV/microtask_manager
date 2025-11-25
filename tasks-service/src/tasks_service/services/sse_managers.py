from asyncio import Queue
from collections import defaultdict
from uuid import UUID

from data.tasks_schemas import TaskReadSchema
from faststream_app import rabbit_broker
from p_database import get_db

from .tasks import TaskService


class SSEManager:
    def __init__(self):
        self._queues: dict[UUID, list[Queue]] = defaultdict(list)

    async def send_user_tasks(self, user_id: UUID) -> None:
        tasks = TaskService(await get_db()).get_all_for(user_id)
        for task in tasks:
            rabbit_broker.publish(
                TaskReadSchema.model_validate(task),
                queue='task.user')

    async def subscribe(self, user_id: UUID) -> Queue:
        rabbit_broker.publish(user_id, queue='user.connected')
        queue = Queue()
        self._queues[user_id].append(queue)
        return queue

    async def unsubscribe(self, user_id: UUID, queue: Queue):
        if user_id not in self._queues:
            return
        try:
            self._queues[user_id].remove(queue)
            if not self._queues[user_id]:
                del self._queues[user_id]
        except ValueError:
            pass
        finally:
            rabbit_broker.publish(user_id, queue='user.disconnected')

    async def broadcast(self, user_id: UUID, task_id: int):
        if user_id not in self._queues:
            return
        for queue in self._queues[user_id][:]:
            try:
                queue.put_nowait(task_id)
            except Exception:
                await self.unsubscribe(user_id, queue)


sse_manager = SSEManager()
