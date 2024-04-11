from .media_model import Media
from uuid import UUID
from sqlmodel import Field, SQLModel, Relationship
from typing import Optional

from app.models.base_model import BaseUUIDModel


class FileMediaBase(SQLModel):
    pass


class FileMedia(BaseUUIDModel, FileMediaBase, table=True):
    message: Optional["Message"] = Relationship(
        back_populates="file", sa_relationship_kwargs={"lazy": "joined"}
    )
    message_id: Optional[UUID] = Field(default=None, foreign_key="Message.id")
    
    media_id: Optional[UUID] = Field(default=None, foreign_key="Media.id")  
    media: Media = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "ImageMedia.media_id==Media.id",
        }
    )