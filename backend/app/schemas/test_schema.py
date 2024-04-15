from uuid import UUID
from typing import Optional, List
from app.models.test_model import TestBase, QuestionBase, AnswerBase
from sqlmodel import  SQLModel


class AnswerCreate(AnswerBase):
    pass


class AnswerUpdate(AnswerBase):
    pass


class AnswerRead(AnswerBase):
    id: UUID
    question_id: UUID


class QuestionCreate(QuestionBase):
    answers: Optional[List[AnswerCreate]]


class QuestionUpdate(QuestionBase):
    pass


class QuestionRead(QuestionBase):
    id: UUID
    test_id: UUID
    answers: Optional[List[AnswerRead]] = []


class TestCreate(TestBase):
    questions: Optional[List[QuestionCreate]]
    

class TestUpdate(TestBase):
    pass


class TestRead(TestBase):
    id: UUID
    task_id: Optional[UUID] = ""
    questions: Optional[List[QuestionRead]] = []

