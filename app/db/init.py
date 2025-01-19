from db.database import engine, Base, get_db
from app.resources.alert_rules.alert_rule_dal import create_alert_rule

async def initialize_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def seed_database():
    async for db in get_db():
        initial_data = [
            {"name": "Tesla Above $800", "threshold_price": 800, "symbol": "TSLA"},
            {"name": "Apple Below $150", "threshold_price": 150, "symbol": "AAPL"},
        ]
        for data in initial_data:
            await create_alert_rule(db, **data)
        break

async def reset_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    await engine.dispose()
