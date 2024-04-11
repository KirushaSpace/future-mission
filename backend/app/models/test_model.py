from sqlmodel import  SQLModel, Relationship
from typing import Optional

from app.models.base_model import BaseUUIDModel


class TestBase(SQLModel):
    title: str
    

class Test(BaseUUIDModel, TestBase, table=True):  
    task: Optional["Task"] = Relationship(
        back_populates="test", sa_relationship_kwargs={"lazy": "joined"}
    )

    questions: Optional["Question"] = Relationship(
        back_populates="test", sa_relationship_kwargs={"lazy": "selecin"} 
    )


class QuestionBase(SQLModel):
    question: str


class Question(BaseUUIDModel, QuestionBase, table=True):
    test: Optional["Test"] = Relationship(
        back_populates="questions", sa_relationship_kwargs={"lazy": "joined"}
    )

    answers: Optional["Answer"] = Relationship(
        back_populates="question", sa_relationship_kwargs={"lazy": "selecin"}
    )


class AnswerBase(SQLModel):
    answer: str
    is_right: bool


class Answer(BaseUUIDModel, AnswerBase, table=True):
    question: Optional["Question"] = Relationship(
        back_populates="answers", sa_relationship_kwargs={"lazy": "joined"}
    )