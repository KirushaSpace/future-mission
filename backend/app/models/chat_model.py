from sqlmodel import  Field, SQLModel, Relationship, Column, JSON
from typing import List, Optional
from uuid import UUID

from app.models.base_model import BaseUUIDModel


class ChatBase(SQLModel):
    title: Optional[str] = Field(nullable=False)
    description: Optional[str] = Field(nullable=False)


class ChatUserLink(BaseUUIDModel, table=True):
    chat_id: Optional[UUID] = Field(
        default=None, foreign_key="Chat.id", primary_key=True
    ) 

    user_id: Optional[UUID] = Field(
        default=None, foreign_key="User.id", primary_key=True
    )


class Chat(BaseUUIDModel, ChatBase, table=True):
    creator: Optional["User"] = Relationship(
        back_populates="chats", sa_relationship_kwargs={"lazy": "joined"}
    )
    creator_id: Optional[UUID] = Field(default=None, foreign_key="User.id")

    users: List["User"] = Relationship(
        back_populates="users_chats", link_model=ChatUserLink, sa_relationship_kwargs={"lazy": "selectin"}
    )

    messages: List["Message"] = Relationship(
        back_populates="chat", sa_relationship_kwargs={"lazy": "selectin"}
    )
