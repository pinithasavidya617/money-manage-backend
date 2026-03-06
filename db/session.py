import os
from typing import AsyncGenerator
from dotenv import load_dotenv
load_dotenv()


from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker
)

DATABASE_URL = os.getenv(
    "DATABASE_URL")

engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    future=True
)

async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session