from fastapi import APIRouter

from app.api.endpoints import chat, message, task, user


api_router = APIRouter()
api_router.include_router(user.router, prefix='/user', tags=['user'])
api_router.include_router(chat.router, prefix='/chat', tags=['chat'])
api_router.include_router(message.router, prefix='/message', tags=['message'])
api_router.include_router(task.router, prefix='/task', tags=['task'])

