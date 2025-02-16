from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from typing import List
from app.resources.alerts.alert_schema import AlertResponse
from app.resources.alerts import alert_service

router = APIRouter(
    prefix="/alerts",
    tags=["Alerts"]
)

@router.get("/", response_model=List[AlertResponse])
async def get_alerts(db: AsyncSession = Depends(get_db)):
    return await alert_service.process_get_all_alerts(db)
