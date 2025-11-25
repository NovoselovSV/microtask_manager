from uuid import UUID
from faststream_app import rabbit_broker
from data.tasks_schemas import TaskSchema
from services.user_tasks_services import user_tasks_service


@rabbit_broker.subscriber('user.connected')
def handle_add_user(user_id: UUID) -> None:
    user_tasks_service.user_add(user_id)


@rabbit_broker.subscriber('user.disconnected')
def handle_remove_user(user_id: UUID) -> None:
    user_tasks_service.user_remove(user_id)


@rabbit_broker.subscriber('task.user')
def handle_user_task(task: TaskSchema) -> None:
    user_tasks_service.task_add(task)
