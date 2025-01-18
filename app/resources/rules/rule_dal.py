from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound
from .rule_model import Rule
import uuid

async def create_rule(db: AsyncSession, name: str, threshold_price: float, symbol: str):
    new_rule = Rule(name=name, threshold_price=threshold_price, symbol=symbol)
    db.add(new_rule)
    await db.commit()
    await db.refresh(new_rule)
    return new_rule

async def get_all_rules(db: AsyncSession):
    result = await db.execute(select(Rule))
    return result.scalars().all()

async def update_rule(db: AsyncSession, rule_id: uuid.UUID, name: str, threshold_price: float, symbol: str):
    result = await db.execute(select(Rule).where(Rule.id == rule_id))
    rule = result.scalar_one_or_none()
    if not rule:
        return None
    rule.name = name
    rule.threshold_price = threshold_price
    rule.symbol = symbol
    await db.commit()
    await db.refresh(rule)
    return rule

async def delete_rule(db: AsyncSession, rule_id: uuid.UUID):
    result = await db.execute(select(Rule).filter(Rule.id == rule_id))
    rule = result.scalars().first()
    if not rule:
        return None
    await db.delete(rule)
    await db.commit()
    return rule
