from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_async_sqlalchemy import SQLAlchemyMiddleware, db
from sqlmodel import text

from app.core.config import settings
from app.api.api import api_router


app = FastAPI()
app.include_router(api_router)


app.add_middleware(
    SQLAlchemyMiddleware,
    db_url=settings.DATABASE_URL,
    engine_args={
        "echo": False,
        "pool_pre_ping": True,
        "pool_size": settings.POOL_SIZE,
        "max_overflow": 64,
    },
)


app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome!"}


async def add_postgresql_extension() -> None:
    async with db():
        query = text("CREATE EXTENSION IF NOT EXISTS pg_trgm")
        return await db.session.execute(query)


@app.on_event("startup")
async def on_startup():
    print("startup fastapi")