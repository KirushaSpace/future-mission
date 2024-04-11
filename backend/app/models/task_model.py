from sqlmodel import  Field, SQLModel, Relationship, Column, JSON
from typing import List, Optional
from uuid import UUID

from app.models.base_model import BaseUUIDModel


class TaskBase(SQLModel):
    type_task: Optional[str] = Field(nullable=False)
    

class Task(BaseUUIDModel, TaskBase, table=True):  
    message: Optional["Message"] = Relationship(
        back_populates="task", sa_relationship_kwargs={"lazy": "joined"}
    )

    test: Optional["Test"] = Relationship(
        back_populates="task", sa_relationship_kwargs={"lazy": "selectin"}
    )

    table: Optional["Table"] = Relationship(
        back_populates="task", sa_relationship_kwargs={"lazy": "selectin"}
    )