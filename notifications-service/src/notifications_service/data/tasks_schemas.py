from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: int
    final_dt: datetime
    creator_id: UUID
