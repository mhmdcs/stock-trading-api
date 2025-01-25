from app.db.base_model import Base
from app.resources.alert_rules.alert_rule_model import AlertRule 
from app.resources.alerts.alert_model import Alert 
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.utils.config import settings

engine = create_async_engine(
    settings.database_connection_string,
    isolation_level="SERIALIZABLE"
    )

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession
)

async def get_db():
    async with async_session() as session:
        yield session
