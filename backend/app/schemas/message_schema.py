from uuid import UUID
from typing import List, Optional

from app.models.message_model import MessageBase
from app.schemas.message_schema import MessageRead
from app.schemas.file_media_schema import FileMediaRead


class MessageCreate(MessageBase):
    chat_id: UUID
    

class MessageUpdate(MessageBase):
    pass


class MessageRead(MessageBase):
    chat_id: UUID
    task: Optional[MessageRead] = None
    user_id: UUID
    id: UUID
    file: Optional[FileMediaRead] = None
    
    class Config:
        from_orm = True