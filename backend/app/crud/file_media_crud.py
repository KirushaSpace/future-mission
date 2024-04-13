from uuid import UUID
from typing import Optional, List
from datetime import datetime
from fastapi_async_sqlalchemy import db
from sqlmodel import select, func, and_
from sqlmodel.ext.asyncio.session import AsyncSession

from app.models.message_model import Message
from app.models.media_model import Media
from app.models.file_media_model import FileMedia
from app.schemas.media_schema import MediaCreate
from app.schemas.file_media_schema import FileMediaCreate, FileMediaUpdate
from app.crud.base_crud import CRUDBase


class CRUDImageMedia(CRUDBase[FileMedia, FileMediaCreate, FileMediaUpdate]):
    async def upload_file(
            self,
            *,
            file: MediaCreate,
            db_session: Optional[AsyncSession] = None
    ) -> Message:
        db_session = db_session or super().get_db().session

        file_media = FileMedia(
            media=Media.from_orm(file),
        )
        db_session.add(file_media)
        await db_session.commit()
        await db_session.refresh(file_media)
        return file_media
    
    
file_media = CRUDImageMedia(FileMedia)