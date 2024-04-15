from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from typing import List, TypeVar, Dict, Union, Any
from sqlmodel import select, and_
import sqlalchemy as sa

from app.api.endpoints import deps
from app.models import Table, User, Col_row
from app.crud import table_crud
from app.schemas.user_schema import RoleEnum
from app.schemas.table_schema import TableCreate, TableRead, TableUpdate, Col_rowCreate, Col_rowRead, Col_rowUpdate


router = APIRouter()


@router.get("")
async def get_multi(
    skip: int = 0,
    limit: int = 100, 
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.user, RoleEnum.admin]))
) -> List[TableRead]:
    query = select(Table).where().offset(skip).limit(limit).order_by(Table.id)
    tables = await table_crud.table.get_multi(query=query)
    return tables


@router.get("/{table_id}")
async def get_table_by_id(
    table_id: UUID,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.user])),
) -> TableRead:
    table = await table_crud.table.get(id=table_id)
    if not table:
        raise HTTPException(status_code=404, detail="table not found")

    return TableRead.model_validate(table)


@router.get("/{table_id}/cols_rows")
async def get_multi_col_row(
    table_id: UUID, 
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.user, RoleEnum.admin]))
) -> List[Col_rowRead]:
    query = select(Col_row).where(Col_row.table_id==table_id).order_by(Col_row.col.desc(), Col_row.row.desc())
    col_rows = await table_crud.col_row.get_multi(query=query)
    return col_rows


@router.post("")
async def create_table(
    table: TableCreate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> TableRead:
    new_table = await table_crud.table.create(obj_in=table)
    return new_table


@router.post("/{table_id}/add_col_row")
async def create_col_row(
    col_row: Col_rowCreate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> Col_rowRead:
    new_col_row = await table_crud.col_row.create(obj_in=col_row)
    return new_col_row


@router.put("/{table_id}")
async def update_table(
    table_id: UUID,
    table: TableUpdate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> TableRead:
    current_table = await table_crud.table.get(id=table_id)
    if not current_table:
        raise HTTPException(status_code=404, detail="table not found")

    table_updated = await table_crud.table.update(obj_new=table, obj_current=current_table)
    return table_updated


@router.put("/col_row/{col_row_id}")
async def update_col_row(
    col_row_id: UUID,
    col_row: Col_rowUpdate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> Col_rowRead:
    current_col_row = await table_crud.col_row.get(id=col_row_id)
    if not current_col_row:
        raise HTTPException(status_code=404, detail="col_row not found")

    col_row_updated = await table_crud.col_row.update(obj_new=col_row, obj_current=current_col_row)
    return col_row_updated


@router.delete("/{table_id}")
async def delete_table(
    table_id: UUID,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
):
    current_table = await table_crud.table.get(id=table_id)
    if not current_table:
        raise HTTPException(status_code=404, detail="table not found")
    
    if current_table.test:
        await table_crud.table.remove(id=current_table.test.id)

    if current_table.table:
        await table_crud.table.remove(id=current_table.table.id)

    table = await table_crud.table.remove(id=table_id)
    return {'table_id': table_id,
            'table': 'deleted'}


@router.delete("/col_row/{col_row_id}")
async def delete_col_row(
    col_row_id: UUID,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
):
    current_col_row = await table_crud.col_row.get(id=col_row_id)
    if not current_col_row:
        raise HTTPException(status_code=404, detail="col_row not found")

    col_row = await table_crud.col_row.remove(id=col_row_id)
    return {'col_row_id': col_row_id,
            'col_row': 'deleted'}