from app.models.test_model import Test, Question, Answer
from app.schemas.test_schema import TestCreate, TestUpdate, QuestionCreate, QuestionUpdate, AnswerCreate, AnswerUpdate 
from app.crud.base_crud import CRUDBase


class CRUDTest(CRUDBase[Test, TestCreate, TestUpdate]):
    pass


test = CRUDTest(Test)


class CRUDQuestion(CRUDBase[Question, QuestionCreate, QuestionUpdate]):
    pass


question = CRUDQuestion(Question)


class CRUDAnswer(CRUDBase[Answer, AnswerCreate, AnswerUpdate]):
    pass


answer = CRUDAnswer(Answer)