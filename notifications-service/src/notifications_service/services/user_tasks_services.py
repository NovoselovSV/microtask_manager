from datetime import datetime


from data.tasks_schemas import TaskSchema
from faststream_app import rabbit_broker
from schedulers import scheduler


class UserTaskService:

    def __init__(self):
        self._connected_users = {}

    def user_add(self, user_id: str):
        if self.is_user_connected(user_id):
            return
        self._connected_users[user_id] = []

    def user_remove(self, user_id: str):
        if not self.is_user_connected(user_id):
            return
        for job_id in self._connected_users[user_id]:
            scheduler.remove_job(job_id)
        self._connected_users.pop(user_id)

    def is_user_connected(self, user_id: str):
        return user_id in self._connected_users

    def is_task_notifiable(self, task: TaskSchema):
        if not self.is_user_connected(task.creator_id):
            return
        if task.final_dt <= datetime.now():
            return
        return True

    def user_task_add(self, task: TaskSchema):
        if not self.is_task_notifiable(task):
            return
        scheduler.add_job(
            self.broadcast_finish_job,
            'date',
            run_date=task.final_dt,
            args=[task.creator_id, task.id],
            id=str(task.id)
        )
        self._connected_users[task.creator_id].append(str(task.id))

    def task_update(self, task: TaskSchema):
        if not self.is_task_notifiable(task):
            return
        task_id = str(task.id)
        if scheduler.get_job(task_id):
            scheduler.remove_job(task_id)
        else:
            self._connected_users[task.creator_id].append(task_id)
        scheduler.add_job(
            self.broadcast_finish_job,
            'date',
            run_date=task.final_dt,
            args=[task.creator_id, task.id],
            id=task_id
        )

    async def broadcast_finish_job(self, user_id: str, task_id: int):
        await rabbit_broker.publish(
            {'user_id': user_id, 'task_id': task_id}, queue='task.end')
        self._connected_users[user_id].remove(str(task_id))


user_tasks_service = UserTaskService()
