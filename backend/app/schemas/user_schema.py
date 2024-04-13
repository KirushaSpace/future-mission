from uuid import UUID
from typing import Optional
from pydantic import BaseModel
from app.models.user_model import UserBase
from enum import Enum


class LoginSchema(BaseModel):
    username: Optional[str]
    password: Optional[str]


class UserCreateWithRole(UserBase):
    password: Optional[str]
    role: str

    class Config:
        hashed_password = None


class UserUpdate(UserBase):
    pass


class UserRead(UserBase):
    id: UUID

    class Config:
        orm_mode = True

    
class RoleEnum(str, Enum):
    admin = "admin"
    user = "user"