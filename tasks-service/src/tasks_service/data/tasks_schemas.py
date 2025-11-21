from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TaskBase(BaseModel):
    description: str
    final_dt: datetime


class TaskRead(TaskBase):
    id: int
    created_at: datetime
    done: bool
    done_dt: datetime | None
    creator_id: UUID


class TaskCreate(TaskBase):
    pass


class TaskEdit(BaseModel):
    description: str | None
    final_dt: datetime | None
    done: bool | None
