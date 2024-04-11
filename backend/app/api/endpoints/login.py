from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import datetime, timedelta

from app.core import security
from app.core.config import settings
from app.crud import user_crud as crud
from app.schemas.token_schema import TokenRead, Token, RefreshToken
from app.schemas.user_schema import LoginSchema


router = APIRouter()


@router.post("")
async def login_access_token(
    form_data: LoginSchema
) -> TokenRead:
    
    user = await crud.user.authenticate(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


@router.post("/access-token")
async def login_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    # redis_client: Redis = Depends(get_redis_client),
) -> TokenRead:

    user = await crud.user.authenticate(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer",
    }