from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from .alert_rule_model import AlertRule
import uuid

async def create_alert_rule(db: AsyncSession, name: str, threshold_price: float, symbol: str):
    new_alert_rule = AlertRule(name=name, threshold_price=threshold_price, symbol=symbol)
    db.add(new_alert_rule)
    await db.commit()
    await db.refresh(new_alert_rule)
    return new_alert_rule

async def get_all_alert_rules(db: AsyncSession):
    result = await db.execute(select(AlertRule))
    return result.scalars().all()

async def update_alert_rule(db: AsyncSession, alert_rule_id: uuid.UUID, name: str, threshold_price: float, symbol: str):
    result = await db.execute(select(AlertRule).where(AlertRule.id == alert_rule_id))
    alert_rule = result.scalar_one_or_none()
    if not alert_rule:
        return None
    alert_rule.name = name
    alert_rule.threshold_price = threshold_price
    alert_rule.symbol = symbol
    await db.commit()
    await db.refresh(alert_rule)
    return alert_rule

async def delete_alert_rule(db: AsyncSession, alert_rule_id: uuid.UUID):
    result = await db.execute(select(AlertRule).filter(AlertRule.id == alert_rule_id))
    alert_rule = result.scalar_one_or_none()
    if not alert_rule:
        return None
    await db.delete(alert_rule)
    await db.commit()
    return alert_rule
