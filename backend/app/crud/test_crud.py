from app.models.test_model import Test, Question, Answer
from app.schemas.test_schema import TestCreate, TestUpdate, QuestionCreate, QuestionUpdate, AnswerCreate, AnswerUpdate 
from app.crud.base_crud import CRUDBase
from typing import Optional, List, Union
from sqlmodel.ext.asyncio.session import AsyncSession


class CRUDTest(CRUDBase[Test, TestCreate, TestUpdate]):
    async def add_question_to_test(
        self,
        *,
        test: Test,
        new_question: Question,
        db_session: Optional[AsyncSession] = None
    ) -> Test:
        db_session = db_session or super().get_db().session
        test.questions.append(new_question)
        db_session.add(test)
        await db_session.commit()
        await db_session.refresh(test)
        return test


test = CRUDTest(Test)


class CRUDQuestion(CRUDBase[Question, QuestionCreate, QuestionUpdate]):
    async def add_answer_to_question(
        self,
        *,
        question: Question,
        new_answer: Answer,
        db_session: Optional[AsyncSession] = None
    ) -> Test:
        db_session = db_session or super().get_db().session
        question.answers.append(new_answer)
        db_session.add(question)
        await db_session.commit()
        await db_session.refresh(question)
        return question


question = CRUDQuestion(Question)


class CRUDAnswer(CRUDBase[Answer, AnswerCreate, AnswerUpdate]):
    pass


answer = CRUDAnswer(Answer)