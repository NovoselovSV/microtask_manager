import asyncio
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from tasks_service.services.tasks import TaskService
from p_database.db import get_db
from services.users import UserService


router = APIRouter()


@router.get('')
async def get_tasks(user: UserService = Depends(UserService.get_current_user),
                    db: AsyncSession = Depends(get_db)):
    user_check_task = asyncio.create_task(user.get_info())
    tasks = await TaskService(db).limit_stmt_by_creator(user.id).get_all()
    try:
        await user_check_task
    except HTTPException:
        raise

    return tasks
