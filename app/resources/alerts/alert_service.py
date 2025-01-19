from uuid import UUID
import uuid
from .alert_dal import create_alert, get_all_alerts
from sqlalchemy.ext.asyncio import AsyncSession

async def process_create_alert(db: AsyncSession, symbol: str, alert_message: str, id: uuid.UUID):
    return await create_alert(db, symbol, alert_message, id)

async def process_get_all_alerts(db: AsyncSession):
    return await get_all_alerts(db)
