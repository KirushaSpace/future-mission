from uuid import UUID
from typing import List, Optional

from app.models.chat_model import ChatBase
from app.schemas.file_media_schema import FileMediaRead
from app.schemas.message_schema import MessageRead


class ChatCreate(ChatBase):
    pass
    

class ChatUpdate(ChatBase):
    pass

class ChatRead(ChatBase):
    file:  Optional[FileMediaRead] = None
    messages: Optional[List[MessageRead]] = []
    id: UUID
    creator_id: UUID
