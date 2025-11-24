from configs.auth import auth_backend, fastapi_users_project
from data.users_schemas import (UserCreateSchema, UserReadSchema,
                                UserUpdateSchema)
from fastapi import APIRouter

from .sse import router as sse_router

router = APIRouter()

router.include_router(
    fastapi_users_project.get_auth_router(auth_backend), prefix='/auth'
)
router.include_router(
    fastapi_users_project.get_register_router(
        UserReadSchema,
        UserCreateSchema),
    prefix='/auth',
)
router.include_router(
    fastapi_users_project.get_reset_password_router(),
    prefix='/auth',
)
router.include_router(
    fastapi_users_project.get_users_router(UserReadSchema, UserUpdateSchema),
)
router.include_router(sse_router)
