from datetime import datetime
from uuid import UUID

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from data.tasks_schemas import TaskSchema
from faststream_app import rabbit_broker


class UserTaskService:

    scheduler = AsyncIOScheduler()

    def __init__(self):
        self._connected_users = {}

    def user_add(self, user_id: UUID):
        if self.is_user_connected(user_id):
            return
        self._connected_users[user_id] = []

    def user_remove(self, user_id: UUID):
        if not self.is_user_connected(user_id):
            return
        for job_id in self._connected_users[user_id]:
            self.scheduler.remove_job(job_id)
        self._connected_users.pop(user_id)

    def is_user_connected(self, user_id: UUID):
        return user_id in self._connected_users

    def user_task_add(self, task: TaskSchema):
        if not self.is_user_connected(task.creator_id):
            return
        if task.final_dt <= datetime.now():
            return
        self.scheduler.add_job(
            self.broadcast_finish_job,
            'date',
            run_date=task.final_dt,
            args=[task.creator_id, task.id],
            id=task.id
        )
        self._connected_users[task.creator_id].append(task.id)

    @staticmethod
    def broadcast_finish_job(user_id, task_id):
        rabbit_broker.publish(
            {'user_id': user_id, 'task_id': task_id}, queue='task.end')


user_tasks_service = UserTaskService()
