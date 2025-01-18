from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from utils.config import settings

engine = create_async_engine(settings.database_connection_string, echo=True)

async_session = sessionmaker(
    bind=engine, expire_on_commit=False, class_=AsyncSession
)

Base = declarative_base()

async def get_db():
    async with async_session() as session:
        yield session
