from typing import Any, Optional
import uuid

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users.db import SQLAlchemyUserDatabase

from data.users import User
from data.users_schemas import UserReadSchema
from services.users import get_user_db
from faststream_app import rabbit_broker

from .settings import Settings

settings = Settings()

SECRET = settings.user_secret

bearer_transport = BearerTransport(tokenUrl='users/auth/login')


class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_update(
        self,
        user: User,
        update_dict: dict[str, Any],
        request: Optional[Request] = None,
    ):
        await rabbit_broker.publish(
            UserReadSchema.model_validate(user),
            queue='update-user',
        )


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=36000)


async def get_user_manager(
        user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

fastapi_users_project = FastAPIUsers[User, uuid.UUID](
    get_user_manager, [auth_backend])

current_active_user = fastapi_users_project.current_user(active=True)
