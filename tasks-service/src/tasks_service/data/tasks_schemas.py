from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TaskBaseSchema(BaseModel):
    description: str
    final_dt: datetime


class TaskReadSchema(TaskBaseSchema):
    id: int
    created_at: datetime
    done: bool
    done_dt: datetime | None
    creator_id: UUID


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskEditSchema(BaseModel):
    description: str | None
    final_dt: datetime | None
    done: bool | None
