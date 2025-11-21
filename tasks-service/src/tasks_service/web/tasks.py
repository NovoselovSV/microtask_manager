import asyncio

from tasks_service.data.tasks_schemas import TaskEdit
from tasks_service.data.users_schemas import UserRead

from data.tasks_schemas import TaskCreate, TaskRead
from fastapi import APIRouter, Depends, HTTPException, status
from p_database.db import get_db
from services.users import UserService
from sqlalchemy.ext.asyncio import AsyncSession

from tasks_service.services.tasks import TaskService

router = APIRouter()


@router.get('', response_model=list[TaskRead])
async def get_tasks(user: UserService = Depends(UserService.get_current_user),
                    db: AsyncSession = Depends(get_db)):
    user_check_task = asyncio.create_task(user.get_info())
    tasks = await TaskService(db).get_all_for(user.id)
    try:
        await user_check_task
    except HTTPException:
        raise

    return tasks


@router.post('', response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
        new_task: TaskCreate,
        user: UserRead = Depends(
            UserService.get_user_info_before_logic),
        db: AsyncSession = Depends(get_db)
):
    return await TaskService(db).create(new_task, user.id)


@router.patch('/{task_id}', response_model=TaskRead)
async def edit_task(
        task_id: int,
        task_data: TaskEdit,
        user: UserRead = Depends(
            UserService.get_user_info_before_logic),
        db: AsyncSession = Depends(get_db)
):
    tasks_service = TaskService(db)
    if not tasks_service.is_task_belong_to_user(task_id, user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return await TaskService(db).edit(task_id, task_data)
