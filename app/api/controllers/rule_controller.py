from fastapi import Depends, APIRouter, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from db.database import get_db
from resources.rules.rule_schema import RuleResponse, RuleCreate, RuleUpdate
from resources.rules.rule_service import process_create_rule, process_get_all_rules, process_update_rule, process_delete_rule

router = APIRouter(
    prefix="/rules",
    tags=["Rules"]
)

@router.post("/", response_model=RuleResponse)
async def create_rule(data: RuleCreate, db: AsyncSession = Depends(get_db)):
    return await process_create_rule(data=data, db=db)

@router.get("/", response_model=List[RuleResponse])
async def get_rules(db: AsyncSession = Depends(get_db)):
    return await process_get_all_rules(db=db)

@router.patch("/{id}", response_model=RuleResponse)
async def update_rule(id: UUID, data: RuleUpdate, db: AsyncSession = Depends(get_db)):
    return await process_update_rule(db=db, id=id, data=data)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_rule(id: UUID, db: AsyncSession = Depends(get_db)):
    await process_delete_rule(db=db, id=id)
