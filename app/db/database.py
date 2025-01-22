from app.db.base_model import Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.utils.config import settings
from contextlib import asynccontextmanager

engine = create_async_engine(
    settings.database_connection_string,
    isolation_level="SERIALIZABLE",
    echo=True)

async_session = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)

async def get_db():
    async with async_session() as session:
        yield session
