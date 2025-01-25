from app.db.database import engine, Base, async_session
from app.resources.alert_rules.alert_rule_dal import create_alert_rule, get_all_alert_rules

async def setup_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def seed_db():
    async with async_session() as db:
        existing_rules = await get_all_alert_rules(db)
        if not existing_rules:  # Only seed if the table is empty
            initial_data = [
                {"name": "Tesla Below $800", "threshold_price": 800, "symbol": "TSLA"},
                {"name": "Apple Above $150", "threshold_price": 150, "symbol": "AAPL"},
            ]
            for data in initial_data:
                await create_alert_rule(db, **data)
    
# just for testing purposes
async def reset_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
