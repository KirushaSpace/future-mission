from uuid import UUID
from typing import List, Optional

from app.models.message_model import MessageBase
from app.schemas.file_media_schema import FileMediaRead
from app.schemas.task_schema import TaskRead


class MessageCreate(MessageBase):
    chat_id: UUID
    

class MessageUpdate(MessageBase):
    pass


class MessageRead(MessageBase):
    chat_id: UUID
    task: Optional[TaskRead] = None
    user_id: UUID
    id: UUID
    file: Optional[FileMediaRead] = None
    
    class Config:
        from_attributes = True