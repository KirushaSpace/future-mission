from uuid import UUID
from typing import Optional, List
from app.models.test_model import TestBase, QuestionBase, AnswerBase


class AnswerCreate(AnswerBase):
    question_id: UUID


class AnswerUpdate(AnswerBase):
    pass


class AnswerRead(AnswerBase):
    id: UUID
    question_id: UUID


class QuestionCreate(QuestionBase):
    test_id: UUID


class QuestionUpdate(QuestionBase):
    pass


class QuestionRead(QuestionBase):
    id: UUID
    test_id: UUID
    answers: Optional[List[AnswerRead]] = []


class TestCreate(TestBase):
    task_id: UUID


class TestUpdate(TestBase):
    pass


class TestRead(TestBase):
    id: UUID
    task_id: UUID
    questions: Optional[List[QuestionRead]] = []
