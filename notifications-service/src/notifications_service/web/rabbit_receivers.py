from services.brokers import rabbit_broker
from data.tasks_schemas import TaskSchema
from services.user_tasks_services import user_tasks_service


@rabbit_broker.subscriber('user.connected')
async def handle_add_user(user_id: str) -> None:
    user_tasks_service.user_add(user_id)


@rabbit_broker.subscriber('user.disconnected')
async def handle_remove_user(user_id: str) -> None:
    user_tasks_service.user_remove(user_id)


@rabbit_broker.subscriber('task.user')
async def handle_user_task(task: TaskSchema) -> None:
    user_tasks_service.user_task_add(task)


@rabbit_broker.subscriber('task.update')
async def handle_task_update(task: TaskSchema) -> None:
    user_tasks_service.task_update(task)
