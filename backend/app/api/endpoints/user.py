from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from app.core import security
from app.core.config import settings

from app.crud import user_crud

from app.models import User

from app.schemas.user_schema import UserCreateWithRole, UserRead, UserUpdate
from app.schemas.token_schema import TokenRead
from app.api.endpoints import deps


router = APIRouter()


@router.post("/registartion", status_code=status.HTTP_201_CREATED)
async def registrate_user(
    new_user: UserCreateWithRole,
) -> TokenRead:
    user = await user_crud.user.create_user(obj_in=new_user)
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/login")
async def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> TokenRead:
    user = await user_crud.user.authenticate(
        username=form_data.username, password=form_data.password
    )

    if not user:
        raise HTTPException(status_code=400, detail="Incorrect login or password")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.get("")
async def get_my_data(
    current_user: User = Depends(deps.get_current_user()),
) -> UserRead:
    return current_user


@router.patch("")
async def update_user(
    new_user: UserUpdate,
    current_user: User = Depends(deps.get_current_user()),
) -> UserRead:
    user_updated = await user_crud.user.update(obj_new=new_user, obj_current=current_user)
    return user_updated


@router.delete("")
async def delete_user(
    user_id: str,
    current_user: User = Depends(deps.get_current_user()),
):
    user_deleted = await user_crud.user.remove(id=user_id)
    return {'user': user_deleted, 'message': 'deleted'}