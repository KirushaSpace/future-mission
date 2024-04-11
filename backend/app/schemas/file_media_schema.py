from app.models.file_media_model import FileMediaBase
from app.schemas.media_schema import MediaRead
from typing import Optional
from uuid import UUID


class FileMediaCreate(FileMediaBase):
    id: UUID
    media: Optional[MediaRead]


class FileMediaUpdate(FileMediaBase):
    pass


class FileMediaRead(FileMediaBase):
    id: UUID
    media: Optional[MediaRead]