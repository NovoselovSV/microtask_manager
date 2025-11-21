from uuid import UUID

from pydantic import BaseModel


class UserRead(BaseModel):
    id: UUID
    is_active: bool
