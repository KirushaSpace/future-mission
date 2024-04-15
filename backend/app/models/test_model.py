from sqlmodel import  SQLModel, Relationship, Field
from typing import Optional, List
from uuid import UUID

from app.models.base_model import BaseUUIDModel


class TestBase(SQLModel):
    title: str
    

class Test(BaseUUIDModel, TestBase, table=True):  
    task: Optional["Task"] = Relationship(
        back_populates="test", sa_relationship_kwargs={"lazy": "joined"}
    )
    task_id: Optional[UUID] = Field(default=None, foreign_key="Task.id")

    questions: List["Question"] = Relationship(
        back_populates="test", sa_relationship_kwargs={"lazy": "selectin"} 
    )


class QuestionBase(SQLModel):
    question: str


class Question(BaseUUIDModel, QuestionBase, table=True):
    test: Optional["Test"] = Relationship(
        back_populates="questions", sa_relationship_kwargs={"lazy": "joined"}
    )
    test_id: Optional[UUID] = Field(default=None, foreign_key="Test.id")

    answers: List["Answer"] = Relationship(
        back_populates="question", sa_relationship_kwargs={"lazy": "selectin"}
    )


class AnswerBase(SQLModel):
    answer: str
    is_right: bool


class Answer(BaseUUIDModel, AnswerBase, table=True):
    question: Optional["Question"] = Relationship(
        back_populates="answers", sa_relationship_kwargs={"lazy": "joined"}
    )
    question_id: Optional[UUID] = Field(default=None, foreign_key="Question.id")