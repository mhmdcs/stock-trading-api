from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from resources.alerts.alert_model import Alert

async def create_alert(db: AsyncSession, symbol: str, rule_id: int):
    new_alert = Alert(symbol=symbol, rule_id=rule_id)
    db.add(new_alert)
    await db.commit()
    await db.refresh(new_alert)
    return new_alert

async def get_all_alerts(db: AsyncSession):
    result = await db.execute(select(Alert))
    return result.scalars().all()
