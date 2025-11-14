from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID

from p_database.db import Base


class User(Base, SQLAlchemyBaseUserTableUUID):

    __tablename__ = 'users'
