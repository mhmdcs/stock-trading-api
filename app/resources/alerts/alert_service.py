from uuid import UUID
import uuid
from app.resources.alerts.alert_dal import create_alert, get_all_alerts
from sqlalchemy.ext.asyncio import AsyncSession

async def process_create_alert(db: AsyncSession, symbol: str, alert_message: str, status:str, priority: str):
    return await create_alert(db, symbol, alert_message, status, priority)

async def process_get_all_alerts(db: AsyncSession):
    return await get_all_alerts(db)
