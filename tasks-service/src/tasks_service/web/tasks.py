import asyncio

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from data.tasks_schemas import TaskCreateSchema, TaskEditSchema, TaskReadSchema
from data.users_schemas import UserReadSchema
from p_database.db import get_db
from services.tasks import TaskService
from services.users import UserService

router = APIRouter(prefix='/v1')


@router.get('', response_model=list[TaskReadSchema])
async def get_tasks(user: UserService = Depends(UserService.get_current_user),
                    db: AsyncSession = Depends(get_db)):
    user_check_task = asyncio.create_task(user.get_info())
    tasks = await TaskService(db).get_all_for(user.id)
    try:
        await user_check_task
    except HTTPException:
        raise

    return tasks


@router.post('', response_model=TaskReadSchema,
             status_code=status.HTTP_201_CREATED)
async def create_task(
        new_task: TaskCreateSchema,
        user: UserReadSchema = Depends(
            UserService.get_user_info_before_logic),
        db: AsyncSession = Depends(get_db)
):
    return await TaskService(db).create(new_task, user.id)


@router.patch('/{task_id}', response_model=TaskReadSchema)
async def edit_task(
        task_id: int,
        task_data: TaskEditSchema,
        user: UserReadSchema = Depends(
            UserService.get_user_info_before_logic),
        db: AsyncSession = Depends(get_db)
):
    tasks_service = TaskService(db)
    if not await tasks_service.is_task_belong_to_user(task_id, user.id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return await TaskService(db).edit(task_id, task_data)
