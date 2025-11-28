from datetime import datetime

from pydantic import BaseModel


class TaskSchema(BaseModel):
    id: int
    final_dt: datetime
    creator_id: str
