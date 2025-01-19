import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from .alert_model import Alert

async def create_alert(db: AsyncSession, symbol: str, alert_message: str, id: uuid.UUID):
    new_alert = Alert(symbol=symbol, alert_message=alert_message, alert_rule_id=id)
    db.add(new_alert)
    await db.commit()
    await db.refresh(new_alert)
    return new_alert

async def get_all_alerts(db: AsyncSession):
    result = await db.execute(select(Alert))
    return result.scalars().all()
