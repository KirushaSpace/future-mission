from uuid import UUID
from typing import Optional, List
from app.models.table_model import TableBase, Col_rowBase


class Col_rowCreate(Col_rowBase):
    table_id: UUID


class Col_rowUpdate(Col_rowBase):
    pass


class Col_rowRead(Col_rowBase):
    id: UUID
    table_id: UUID


class TableCreate(TableBase):
    pass


class TableUpdate(TableBase):
    task_id: Optional[UUID]


class TableRead(TableBase):
    id: UUID
    task_id: Optional[UUID] = ""
    cols_rows: Optional[List[Col_rowRead]] = []