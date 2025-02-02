import contextlib
from typing import AsyncGenerator
from app.db.base_model import Base
from app.resources.alert_rules.alert_rule_model import AlertRule 
from app.resources.alerts.alert_model import Alert 
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from app.utils.config import settings
from app.resources.alert_rules.alert_rule_dal import create_alert_rule, get_all_alert_rules
import aiofiles

engine = create_async_engine(
    settings.database_connection_string,
    isolation_level="SERIALIZABLE"
    )

async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db():
    async with async_session() as session:
        yield session
        
# we use this only in processes like celery and rabbitmq consumer that shouldn't keep the engine leaking with every task
@contextlib.asynccontextmanager
async def get_db_and_dispose_engine() -> AsyncGenerator:
    try:
        db = async_session()
        yield db
    finally:
        await db.close()
        await engine.dispose()

async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as db:
        async with aiofiles.open("dev_setup/sql/seed.sql", "r") as file:
            sql_script = await file.read()

        try:
            await db.execute(text(sql_script))
            await db.commit()
        except Exception as e:
            print(f"failed to seed database: {e}")
    
# just for testing purposes
async def reset_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()