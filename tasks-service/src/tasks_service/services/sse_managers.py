from asyncio import Queue
from collections import defaultdict

from data.tasks_schemas import TaskReadSchema
from faststream_app import rabbit_router
from p_database.db import get_db

from .tasks import TaskService


class SSEManager:
    def __init__(self):
        self._queues: dict[str, list[Queue]] = defaultdict(list)

    async def send_user_tasks(self, user_id: str) -> None:
        tasks = await (TaskService(await anext(get_db())).get_all_for(user_id))
        for task in tasks:
            await rabbit_router.broker.publish(
                TaskReadSchema.model_validate(task).model_dump(),
                queue='task.user')

    async def subscribe(self, user_id: str) -> Queue:
        await rabbit_router.broker.publish(user_id, queue='user.connected')
        await self.send_user_tasks(user_id)
        queue = Queue()
        self._queues[user_id].append(queue)
        return queue

    async def unsubscribe(self, user_id: str, queue: Queue):
        if user_id not in self._queues:
            return
        try:
            self._queues[user_id].remove(queue)
            if not self._queues[user_id]:
                del self._queues[user_id]
        except ValueError:
            pass
        finally:
            await rabbit_router.broker.publish(user_id,
                                               queue='user.disconnected')

    async def broadcast(self, user_id: str, task_id: int):
        if user_id not in self._queues:
            return
        try:
            for queue in self._queues[user_id][:]:
                queue.put_nowait(task_id)
        except Exception:
            await self.unsubscribe(user_id, queue)


sse_manager = SSEManager()
