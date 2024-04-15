from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from app.models.user_model import UserBase
from enum import Enum


class LoginSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]


class UserCreate(UserBase):
    password: Optional[str]

    class Config:
        hashed_password = None


class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    id: UUID

    class Config:
        from_attributes = True

    
class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"