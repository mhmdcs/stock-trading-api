from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.resources.alert_rules.alert_rule_dal import create_alert_rule, get_all_alert_rules, update_alert_rule, delete_alert_rule
from app.resources.alert_rules.alert_rule_schema import AlertRuleCreate, AlertRuleUpdate
from uuid import UUID

async def process_create_alert_rule(db: AsyncSession, data: AlertRuleCreate):
    alert_rule = await create_alert_rule(db, data.name, data.threshold_price, data.symbol)
    if not alert_rule:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Alert Rule with this name already exists")
    return alert_rule

async def process_get_all_alert_rules(db: AsyncSession):
    return await get_all_alert_rules(db)

async def process_update_alert_rule(db: AsyncSession, id: UUID, data: AlertRuleUpdate):
    alert_rule = await update_alert_rule(db, id, data.name, data.threshold_price, data.symbol)
    if not alert_rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert Rule not found")
    return alert_rule

async def process_delete_alert_rule(db: AsyncSession, id: UUID):
    alert_rule = await delete_alert_rule(db, id)
    if not alert_rule:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Alert Rule not found")
    return alert_rule
