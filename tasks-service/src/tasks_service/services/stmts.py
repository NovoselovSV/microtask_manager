from uuid import UUID

from sqlalchemy import select, update

from p_database.db import Base
from data.tasks import Task


class Stmt:

    def __init__(self, model: Base):
        self._model = model
        self._stmt = None

    def __getattr__(self, name):
        return getattr(self._stmt, name)

    def set_to_update(self):
        self._stmt = update(self._model)
        return self

    def set_to_select(self):
        self._stmt = select(self._model)
        return self

    @property
    def raw_stmt(self):
        return self._stmt


class TaskStmt(Stmt):

    def __init__(self):
        super().__init__(Task)

    def limit_by_creator(self, user_id: UUID):
        self._stmt = self._stmt.where(Task.creator_id == user_id)
        return self

    def limit_by_id(self, id: int):
        self._stmt = self._stmt.where(Task.id == id)
        return self

    def limit_to_one_for_user(self, id: int, user_id: UUID):
        self.limit_by_creator(user_id)
        self.limit_by_id(id)
        return self
