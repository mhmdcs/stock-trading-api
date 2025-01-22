from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.db.database import get_db
from app.resources.alert_rules.alert_rule_schema import AlertRuleResponse, AlertRuleCreate, AlertRuleUpdate
from app.resources.alert_rules.alert_rule_service import process_create_alert_rule, process_get_all_alert_rules, process_update_alert_rule, process_delete_alert_rule

router = APIRouter(
    prefix="/alert_rules",
    tags=["Alert Rules"]
)

@router.post("/", response_model=AlertRuleResponse)
async def create_alert_rule(data: AlertRuleCreate, db: AsyncSession = Depends(get_db)):
    return await process_create_alert_rule(data=data, db=db)

@router.get("/", response_model=List[AlertRuleResponse])
async def get_alert_rules(db: AsyncSession = Depends(get_db)):
    return await process_get_all_alert_rules(db=db)

@router.patch("/{id}", response_model=AlertRuleResponse)
async def update_alert_rule(id: UUID, data: AlertRuleUpdate, db: AsyncSession = Depends(get_db)):
    return await process_update_alert_rule(db=db, id=id, data=data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert_rule(id: UUID, db: AsyncSession = Depends(get_db)):
    await process_delete_alert_rule(db=db, id=id)
