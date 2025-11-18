from fastapi import APIRouter

from configs.auth import auth_backend, fastapi_users_project
from data.users_schemas import UserCreate, UserRead, UserUpdate
from .sse import router as sse_router

router = APIRouter(prefix='/users')

router.include_router(
    fastapi_users_project.get_auth_router(auth_backend), prefix='/auth'
)
router.include_router(
    fastapi_users_project.get_register_router(UserRead, UserCreate),
    prefix='/auth',
)
router.include_router(
    fastapi_users_project.get_reset_password_router(),
    prefix='/auth',
)
router.include_router(
    fastapi_users_project.get_users_router(UserRead, UserUpdate),
)
router.include_router(sse_router)
