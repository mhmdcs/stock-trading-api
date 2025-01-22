import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.resources.alerts.alert_model import Alert

async def create_alert(db: AsyncSession, symbol: str, alert_message: str, status: str, priority: str, id: uuid.UUID):
    new_alert = Alert(symbol=symbol, alert_message=alert_message, alert_rule_id=id, status=status, priority=priority)
    db.add(new_alert)
    await db.commit()
    await db.refresh(new_alert)
    return new_alert

async def get_all_alerts(db: AsyncSession):
    result = await db.execute(select(Alert))
    return result.scalars().all()
