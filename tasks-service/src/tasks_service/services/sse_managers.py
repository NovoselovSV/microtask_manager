from asyncio import Queue
from collections import defaultdict

from p_database.db import get_db
from .rabbit_service import RabbitService
from .tasks import TaskService


class SSEManager:

    def __init__(self):
        self._queues: dict[str, list[Queue]] = defaultdict(list)
        self.rabbit_service = RabbitService()

    async def subscribe(self, user_id: str) -> Queue:
        await self.rabbit_service.send_user_connected(user_id)
        try:
            db = await anext(get_db())
            await self.rabbit_service.send_user_tasks(
                await (TaskService(db).get_all_for(user_id))
            )
        finally:
            await db.aclose()
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
            await self.rabbit_service.send_user_disconnected(user_id)

    async def broadcast(self, user_id: str, task_id: int):
        if user_id not in self._queues:
            return
        try:
            for queue in self._queues[user_id][:]:
                queue.put_nowait(task_id)
        except Exception:
            await self.unsubscribe(user_id, queue)


sse_manager = SSEManager()
