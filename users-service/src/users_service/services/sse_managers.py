from asyncio import Queue
from collections import defaultdict
from uuid import UUID

from users_service.data.users_schemas import UserReadSchema


class SSEManager:
    def __init__(self):
        self._queues: dict[UUID, list[Queue]] = defaultdict(list)

    async def subscribe(self, user_id: UUID) -> Queue:
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

    async def broadcast(self, user_id: UUID, user: UserReadSchema):
        if user_id not in self._queues:
            return
        for queue in self._queues[user_id][:]:
            try:
                queue.put_nowait(user)
            except Exception:
                await self.unsubscribe(user_id, queue)


sse_manager = SSEManager()
