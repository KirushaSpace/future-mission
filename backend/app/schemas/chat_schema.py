from uuid import UUID
from typing import List, Optional

from app.models.chat_model import ChatBase
from app.schemas.message_schema import MessageRead
from app.schemas.user_schema import UserRead


class ChatCreate(ChatBase):
    creator_id: UUID
    

class ChatUpdate(ChatBase):
    pass


class ChatRead(ChatBase):
    messages: Optional[List[MessageRead]] = []
    users: Optional[List[UserRead]] = []
    id: UUID
    creator_id: UUID

    class Config:
        from_orm = True