from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .rule_dal import create_rule, get_all_rules, update_rule, delete_rule
from app.resources.rules.rule_schema import RuleCreate, RuleUpdate

async def process_create_rule(data: RuleCreate, db: AsyncSession):
    return await create_rule(db, data.name, data.threshold_price, data.symbol)

async def process_get_all_rules(db: AsyncSession):
    return await get_all_rules(db)

async def process_update_rule(id: int, data: RuleUpdate, db: AsyncSession):
    rule = await update_rule(db, id, data.name, data.threshold_price, data.symbol)
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")
    return rule

async def process_delete_rule(id: int, db: AsyncSession):
    rule = await delete_rule(db, id)
    if not rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Rule not found")
    return rule
