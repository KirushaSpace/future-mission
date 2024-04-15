from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from typing import List, TypeVar, Dict, Union, Any
from sqlmodel import select, and_
import sqlalchemy as sa

from app.api.endpoints import deps
from app.models import User, Test, Question, Answer
from app.crud import test_crud
from app.schemas.user_schema import RoleEnum
from app.schemas.test_schema import (
    TestCreate, TestRead, TestUpdate,
    QuestionCreate, QuestionRead, QuestionUpdate,
    AnswerCreate, AnswerRead, AnswerUpdate
)

router = APIRouter()


@router.get("")
async def get_multi(
    skip: int = 0,
    limit: int = 100, 
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.user, RoleEnum.admin]))
) -> List[TestRead]:
    query = select(Test).where().offset(skip).limit(limit).order_by(Test.id)
    tests = await test_crud.test.get_multi(query=query)
    return tests


@router.get("/{test_id}")
async def get_test_by_id(
    test_id: UUID,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.user])),
) -> TestRead:
    test = await test_crud.test.get(id=test_id)
    if not test:
        raise HTTPException(status_code=404, detail="test not found")

    return TestRead.model_validate(test)


@router.get("/question/{question_id}")
async def get_question_by_id(
    question_id: UUID,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.user])),
) -> QuestionRead:
    question = await test_crud.question.get(id=question_id)
    if not question:
        raise HTTPException(status_code=404, detail="test not found")

    return QuestionRead.model_validate(question)


@router.get("/answer/{answer_id}")
async def get_answer_by_id(
    answer_id: UUID,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin, RoleEnum.user])),
) -> AnswerRead:
    answer = await test_crud.answer.get(id=answer_id)
    if not answer:
        raise HTTPException(status_code=404, detail="answer not found")

    return AnswerRead.model_validate(answer)


@router.post("")
async def create_test(
    test: TestCreate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> TestRead:
    questions = test.questions
    del test.questions
    new_test = await test_crud.test.create(obj_in=test)

    for question in questions:
        answers = question.answers
        del question.answers
        new_question = await test_crud.question.create(obj_in=question)

        for answer in answers:
            new_answer = await test_crud.answer.create(obj_in=answer)
            new_question = await test_crud.question.add_answer_to_question(question=new_question, new_answer=new_answer)

        new_test = await test_crud.test.add_question_to_test(test=new_test, new_question=new_question)
    
    return new_test


@router.put("/{test_id}")
async def update_test(
    test_id: UUID,
    test: TestUpdate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> TestRead:
    current_test = await test_crud.test.get(id=test_id)
    if not current_test:
        raise HTTPException(status_code=404, detail="test not found")

    test_updated = await test_crud.test.update(obj_new=test, obj_current=current_test)
    return test_updated


@router.put("/question/{question_id}")
async def update_question(
    question_id: UUID,
    question: QuestionUpdate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> QuestionRead:
    current_question = await test_crud.question.get(id=question_id)
    if not current_question:
        raise HTTPException(status_code=404, detail="question not found")

    question_updated = await test_crud.question.update(obj_new=question, obj_current=current_question)
    return question_updated


@router.put("/answer/{answer_id}")
async def update_answer(
    answer_id: UUID,
    answer: AnswerUpdate,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
) -> AnswerRead:
    current_answer = await test_crud.answer.get(id=answer_id)
    if not current_answer:
        raise HTTPException(status_code=404, detail="answer not found")

    answer_updated = await test_crud.answer.update(obj_new=answer, obj_current=current_answer)
    return answer_updated


@router.delete("/{test_id}")
async def delete_test(
    test_id: UUID,
    current_user: User = Depends(deps.get_current_user(required_roles=[RoleEnum.admin])),
):
    current_test = await test_crud.test.get(id=test_id)
    if not current_test:
        raise HTTPException(status_code=404, detail="test not found")
    
    if current_test.test:
        await test_crud.test.remove(id=current_test.test.id)

    if current_test.test:
        await test_crud.test.remove(id=current_test.test.id)

    test = await test_crud.test.remove(id=test_id)
    return {'test_id': test_id,
            'test': 'deleted'}