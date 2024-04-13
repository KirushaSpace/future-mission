from app.models import Chat
from app.schemas.chat_schema import ChatCreate, ChatUpdate
from app.crud.base_crud import CRUDBase


class CRUDChat(CRUDBase[Chat, ChatCreate, ChatUpdate]):
    pass


chat = CRUDChat(Chat)