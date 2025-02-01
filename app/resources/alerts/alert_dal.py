import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.resources.alerts.alert_model import Alert
from app.resources.alert_rules.alert_rule_model import AlertRule

async def create_alert(db: AsyncSession, symbol: str, alert_message: str, status, priority: str):
    stmt = (
        select(AlertRule.id)
        .where(AlertRule.symbol == symbol)
        .limit(1)
    )

    result = await db.execute(stmt)
    alert_rule_id = result.scalar()

    if alert_rule_id:
        new_alert = Alert(symbol=symbol, alert_message=alert_message, status=status, priority=priority, alert_rule_id=alert_rule_id)
        db.add(new_alert)
        await db.commit()
        return new_alert
    else:
        raise ValueError(f"No AlertRule found for symbol {symbol}")
    
async def get_all_alerts(db: AsyncSession):
    result = await db.execute(select(Alert))
    return result.scalars().all()