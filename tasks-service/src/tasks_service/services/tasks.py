from datetime import datetime
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from data.tasks import Task
from data.tasks_schemas import TaskCreateSchema, TaskEditSchema
from services.stmts import TaskStmt


class TaskService:

    def __init__(self, db: AsyncSession):
        self.db = db

    def get_stmt(self):
        return TaskStmt()

    async def is_task_belong_to_user(self, task_id: int, user_id: UUID):
        result = await self.db.execute(self.get_stmt()
                                       .set_to_select()
                                       .limit_by_creator(user_id)
                                       .limit_by_id(task_id)
                                       .raw_stmt)
        return result.scalar_one_or_none()

    async def get_by_id(self, task_id: int):
        result = await self.db.execute(self.get_stmt()
                                       .set_to_select()
                                       .limit_by_id(task_id)
                                       .raw_stmt)
        return result.scalar_one_or_none()

    async def get_all_for(self, user_id: UUID):
        result = await self.db.execute(self.get_stmt()
                                       .set_to_select()
                                       .limit_by_creator(user_id)
                                       .raw_stmt)
        return result.scalars().all()

    async def create(self, task_data: TaskCreateSchema, user_id: UUID):
        task = Task(
            description=task_data.description,
            done=False,
            final_dt=task_data.final_dt.replace(tzinfo=None),
            creator_id=user_id)
        self.db.add(task)
        await self.db.commit()
        return task

    async def edit(self, task_id: int, task_data: TaskEditSchema):
        updated_values = task_data.model_dump(exclude_unset=True)
        prev_state = await self.get_by_id(task_id)
        if not prev_state:
            return
        if task_data.done and prev_state.done != task_data.done:
            updated_values['done_dt'] = datetime.now()
        await self.db.execute(
            self.get_stmt()
            .set_to_update()
            .limit_by_id(task_id)
            .raw_stmt
            .values(**updated_values)
            )
        await self.db.commit()
        return await self.get_by_id(task_id)
