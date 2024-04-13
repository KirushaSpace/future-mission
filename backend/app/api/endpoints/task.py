from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from typing import List, TypeVar, Dict, Union, Any
from sqlmodel import select, and_
import sqlalchemy as sa

from app.api.endpoints import deps
from app.models import Task, Test, Table, User
from app.crud import task_crud, test_crud, table_crud
from app.schemas.user_schema import RoleEnum
from app.schemas.task_schema import TaskCreate, TaskRead, TaskUpdate


router = APIRouter()


@router.get("")
async def get_multi(
    skip: int = 0,
    limit: int = 100, 
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.user, RoleEnum.admin]))
) -> List[TaskRead]:
    query = select(Task).where().offset(skip).limit(limit).order_by(Task.id)
    tasks = await task_crud.task.get_multi(query=query)
    return tasks


@router.get("/{task_id}")
async def get_task_by_id(
    task_id: UUID,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.user])),
) -> TaskRead:
    task = await task_crud.task.get(id=task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return TaskRead.model_validate(task)


@router.post("")
async def create_task(
    task: TaskCreate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> TaskRead:
    new_task = await task_crud.task.create(obj_in=task, user_id=current_user.id)
    return new_task


@router.put("/{task_id}")
async def update_task(
    task_id: UUID,
    task: TaskUpdate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> TaskRead:
    current_task = await task_crud.task.get(id=task_id)
    if not current_task:
        raise HTTPException(status_code=404, detail="Task not found")

    task_updated = await task_crud.task.update(obj_new=task, obj_current=current_task)
    return task_updated


@router.delete("/{task_id}")
async def delete_task(
    task_id: UUID,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
):
    current_task = await task_crud.task.get(id=task_id)
    if not current_task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if current_task.test:
        await task_crud.task.remove(id=current_task.test.id)

    if current_task.table:
        await task_crud.task.remove(id=current_task.table.id)

    task = await task_crud.task.remove(id=task_id)
    return {'chat_id': task_id,
            'task': 'deleted'}