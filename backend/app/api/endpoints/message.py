from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from typing import List, TypeVar, Dict, Union, Any
from sqlmodel import select, and_
import sqlalchemy as sa

from app.api.endpoints import deps
from app.models import User, Message
from app.crud import message_crud, task_crud
from app.schemas.user_schema import RoleEnum
from app.schemas.message_schema import MessageCreate, MessageRead, MessageUpdate


router = APIRouter()


@router.get("")
async def get_multi(
    skip: int = 0,
    limit: int = 100, 
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.user, RoleEnum.admin]))
) -> List[MessageRead]:
    query = select(Message).where().offset(skip).limit(limit).order_by(Message.id)
    messages = await message_crud.message.get_multi(query=query)
    return messages


@router.get("/{message_id}")
async def get_message_by_id(
    message_id: UUID,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.user])),
) -> MessageRead:
    message = await message_crud.message.get(id=message_id)
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")

    return MessageRead.model_validate(message)


@router.post("")
async def create_message(
    message: MessageCreate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> MessageRead:
    new_message = await message_crud.message.create(obj_in=message, user_id=current_user.id)
    return new_message


@router.put("/{message_id}")
async def update_message(
    message_id: UUID,
    message: MessageUpdate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> MessageRead:
    current_message = await message_crud.message.get(id=message_id)
    if not current_message:
        raise HTTPException(status_code=404, detail="Message not found")

    message_updated = await message_crud.message.update(obj_new=message, obj_current=current_message)
    return message_updated


@router.delete("/{message_id}")
async def delete_message(
    message_id: UUID,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
):
    current_message = await message_crud.message.get(id=message_id)
    if not current_message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if current_message.task:
        await task_crud.task.remove(id=current_message.task.id)

    message = await message_crud.message.remove(id=message_id)
    return {'chat_id': message_id,
            'message': 'deleted'}