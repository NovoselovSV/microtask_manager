import json
from asyncio import wait_for

from fastapi import APIRouter, Depends
from sse_starlette.sse import EventSourceResponse
from tasks_service.services.users import UserService

from services.sse_managers import sse_manager

router = APIRouter(prefix='/v1/sse')


@router.get('')
async def sse_notifications(
        user: UserService = Depends(UserService.get_current_user)):
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
