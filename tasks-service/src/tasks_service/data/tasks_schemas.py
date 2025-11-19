from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: int
    created_at: datetime
    done: bool | None
    done_dt: datetime | None
    final_dt: datetime | None
    creator_id: UUID
