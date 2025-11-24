import uuid

from fastapi_users import schemas


class UserReadSchema(schemas.BaseUser[uuid.UUID]):
    pass


class UserCreateSchema(schemas.BaseUserCreate):
    pass


class UserUpdateSchema(schemas.BaseUserUpdate):
    pass
