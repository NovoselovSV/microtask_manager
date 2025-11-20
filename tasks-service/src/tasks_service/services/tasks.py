from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from tasks_service.data.tasks import Task


class TaskService:

    def __init__(self, db: AsyncSession):
        self.db = db
        self.stmt = select(Task)

    def limit_stmt_by_creator(self, user_id: str):
        self.stmt = self.stmt.where(Task.creator_id == user_id)

    async def get_all(self):
        result = await self.db.execute(self.stmt)
        return result.scalars().all()
