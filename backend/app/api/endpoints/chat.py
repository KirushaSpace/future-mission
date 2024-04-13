from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from typing import List, TypeVar, Dict, Union, Any
from sqlmodel import select, and_
import sqlalchemy as sa

from app.api.endpoints import deps
from app.models import User, Chat, Message
from app.crud import chat_crud, message_crud
from app.schemas.user_schema import RoleEnum
from app.schemas.chat_schema import ChatCreate, ChatRead, ChatUpdate


router = APIRouter()


@router.get("")
async def get_multi(
    skip: int = 0,
    limit: int = 100, 
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.user, RoleEnum.admin]))
) -> List[ChatRead]:
    query = select(Chat).where().offset(skip).limit(limit).order_by(Chat.id)
    chats = await chat_crud.chat.get_multi(query=query)
    return chats


@router.get("/{chat_id}")
async def get_chat_by_id(
    chat_id: UUID,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.user])),
) -> ChatRead:
    chat = await chat_crud.chat.get(id=chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    return ChatRead.model_validate(chat)


@router.post("")
async def create_chat(
    chat: ChatCreate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> ChatRead:
    new_chat = await chat_crud.chat.create(obj_in=chat, user_id=current_user.id)
    return new_chat


@router.put("/{chat_id}")
async def update_chat(
    chat_id: UUID,
    message: ChatUpdate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> ChatRead:
    current_chat = await chat_crud.chat.get(id=chat_id)
    if not current_chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    chat_updated = await chat_crud.chat.update(obj_new=message, obj_current=current_chat)
    return chat_updated


@router.delete("/{chat_id}")
async def delete_chat(
    chat_id: UUID,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
):
    current_chat = await chat_crud.chat.get(id=chat_id)
    if not current_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    for message in current_chat.messages:
        await message_crud.message.remove(id=message.id)

    chat = await chat_crud.chat.remove(id=chat_id)
    return {'chat_id': chat_id,
            'message': 'deleted'}