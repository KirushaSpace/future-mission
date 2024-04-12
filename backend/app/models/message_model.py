from sqlmodel import  Field, SQLModel, Relationship, Column, JSON
from typing import List, Optional
from uuid import UUID

from app.models.base_model import BaseUUIDModel


class MessageBase(SQLModel):
    message_body: Optional[str] = Field(default=None)
    


class Message(BaseUUIDModel, MessageBase, table=True):  
    chat: Optional["Chat"] = Relationship(
        back_populates="messages", sa_relationship_kwargs={"lazy": "joined"}
    )
    chat_id: Optional[UUID] = Field(default=None, foreign_key="Chat.id")

    user: Optional["User"] = Relationship(
        back_populates="masseges", sa_relationship_kwargs={"lazy": "joined"}
    )
    user_id: Optional[UUID] = Field(default=None, foreign_key="User.id")

    task: Optional["Task"] = Relationship(
        back_populates="message", sa_relationship_kwargs={"lazy": "selectin"}
    )

    file: List["FileMedia"] = Relationship(
        back_populates="message", sa_relationship_kwargs={"lazy": "selectin"}
    )