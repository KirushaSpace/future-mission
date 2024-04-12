from uuid import UUID
from typing import List, Optional
from app.models.task_model import TaskBase

from app.schemas.test_schema import TestRead
from app.schemas.table_schema import TableRead


class TaskCreate(TaskBase):
    message_id: UUID


class TaskUpdate(TaskBase):
    pass


class TaskRead(TaskBase):
    id: UUID
    message_id: UUID

    test: Optional[TestRead] = None
    table: Optional[TableRead] = None