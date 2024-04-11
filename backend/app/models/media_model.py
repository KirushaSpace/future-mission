from sqlmodel import SQLModel
from typing import Optional

from app.models.base_model import BaseUUIDModel


class MediaBase(SQLModel):
    title: Optional[str]
    decription: Optional[str]
    path: Optional[str]


class Media(BaseUUIDModel, MediaBase, table=True):
    pass