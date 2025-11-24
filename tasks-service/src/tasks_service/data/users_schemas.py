from uuid import UUID

from pydantic import BaseModel


class UserReadSchema(BaseModel):
    id: UUID
    is_active: bool
