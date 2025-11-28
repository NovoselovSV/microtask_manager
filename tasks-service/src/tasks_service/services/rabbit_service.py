from collections.abc import Iterable

from configs.settings import Settings
from data.tasks import Task
from data.tasks_schemas import TaskReadSchema
from faststream_app import rabbit_router

settings = Settings()


class RabbitService:

    router = rabbit_router

    async def publish(self, data: dict, queue: str):
        return await self.router.broker.publish(data, queue=queue)

    async def send_user_task(self, task: Task):
        await self.publish(
            TaskReadSchema.model_validate(task).model_dump(),
            settings.task_user_queue)

    async def send_user_tasks(self, tasks: Iterable[Task]) -> None:
        for task in tasks:
            await self.send_user_task(task)

    async def send_user_connected(self, user_id: str):
        await self.publish(user_id,
                           settings.user_connected_queue)

    async def send_user_disconnected(self, user_id: str):
        await self.publish(
            user_id,
            settings.user_disconnected_queue)

    async def send_task_update(self, task: Task):
        await self.publish(
            TaskReadSchema.model_validate(task).model_dump(),
            settings.task_update_queue)
