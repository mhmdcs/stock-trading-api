from .model_base import Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from utils.config import settings
from resources.alerts.alert_model import Alert
from app.resources.alert_rules.alert_rule_model import AlertRule

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
