from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TaskBaseSchema(BaseModel):
    description: str
    final_dt: datetime

    model_config = {'from_attributes': True}


class TaskReadSchema(TaskBaseSchema):
    id: int
    created_at: datetime
    done: bool
    done_dt: datetime | None
    creator_id: UUID


class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskEditSchema(BaseModel):
    description: str | None = None
    final_dt: datetime | None = None
    done: bool | None = None
