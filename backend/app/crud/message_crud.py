from app.models.message_model import Message
from app.schemas.message_schema import MessageCreate, MessageUpdate
from app.crud.base_crud import CRUDBase


class CRUDMessage(CRUDBase[Message, MessageCreate, MessageUpdate]):
    pass


message = CRUDMessage(Message)