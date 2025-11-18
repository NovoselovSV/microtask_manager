import json
from asyncio import wait_for
from typing import Annotated

from fastapi import APIRouter, Depends
from sse_starlette.sse import EventSourceResponse
from users_service.data.users import User

from configs.auth import current_active_user
from .sse_managers import sse_manager

router = APIRouter(prefix='/sse')


@router.get('')
async def sse_notifications(
        user: Annotated[User, Depends(current_active_user)]):
    queue = await sse_manager.subscribe(user.id)

    async def event_generator():
        try:
            while True:
                try:
                    data = await wait_for(queue.get(), timeout=30.0)
                    yield {
                        'event': 'notification',
                        'data': json.dumps(data, ensure_ascii=False)
                    }
                except TimeoutError:
                    yield {'data': ''}
        finally:
            await sse_manager.unsubscribe(user.id, queue)

    return EventSourceResponse(event_generator())
