from app.models.table_model import Table, Col_row
from app.schemas.table_schema import TableCreate, TableUpdate, Col_rowCreate, Col_rowUpdate
from app.crud.base_crud import CRUDBase


class CRUDTable(CRUDBase[Table, TableCreate, TableUpdate]):
    pass


table = CRUDTable(Table)


class CRUDCol_row(CRUDBase[Col_row, Col_rowCreate, Col_rowUpdate]):
    pass


col_row = CRUDCol_row(Col_row)