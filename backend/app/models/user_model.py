from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from app.models.chat_model import ChatUserLink
from app.models.base_model import BaseUUIDModel


class UserBase(SQLModel):
    first_name: str
    last_name: str
    username: str = Field(
        nullable=True, index=True, sa_column_kwargs={"unique": True}
    )
    role: str = Field(default='user')
    is_active: bool


class User(BaseUUIDModel, UserBase, table=True):
    hashed_password: Optional[str] = Field(default=None, nullable=False, index=True)

    chats: List["Chat"] = Relationship(
        back_populates="creator", sa_relationship_kwargs={"lazy": "selectin"}
    )
    
    users_chats: Optional["Chat"] = Relationship(
        back_populates="users", link_model=ChatUserLink, sa_relationship_kwargs={"lazy": "joined"}
    )

    messages: List["Message"] = Relationship(
        back_populates="user", sa_relationship_kwargs={"lazy": "selectin"}
    )

    