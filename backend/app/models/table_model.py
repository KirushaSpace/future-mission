from sqlmodel import  Field, SQLModel, Relationship, Column, JSON
from typing import List, Optional
from uuid import UUID

from app.models.base_model import BaseUUIDModel


class TableBase(SQLModel):
    title: Optional[str] = Field(nullable=False)
    
    
class Table(BaseUUIDModel, TableBase, table=True):  
    task: Optional["Task"] = Relationship(
        back_populates="table", sa_relationship_kwargs={"lazy": "joined"}
    )

    cols_rows: Optional["Col_row"] = Relationship(
        back_populates="table", sa_relationship_kwargs={"lazy": "selectin"}     
    )


class Col_rowBase(SQLModel):
    col: int
    row: int
    text: str


class Col_row(BaseUUIDModel, Col_rowBase, table=True):
    table: Optional["Table"] = Relationship(
        back_populates="cols_rows", sa_relationship_kwargs={"lazy": "joined"}
    )