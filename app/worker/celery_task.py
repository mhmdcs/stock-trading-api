from celery_app import celery
from app.resources.market.market_service import process_market_prices_data
from app.resources.alert_rules.alert_rule_service import process_get_all_alert_rules
from app.core.message_publisher import publish_threshold_alert
from app.db.database import async_session
import asyncio

@celery.task
def fetch_and_check_market_data():
    async def async_task():
        async with async_session() as db:
            alert_rules = await process_get_all_alert_rules(db)

            symbols = [rule.symbol for rule in alert_rules]

            market_data = await process_market_prices_data({"symbols": symbols})

            for rule in alert_rules:
                for market_item in market_data:
                    if rule.symbol == market_item["symbol"] and market_item["price"] is not None:
                        if (
                            (rule.threshold_price >= market_item["price"] and "Below" in rule.name)
                            or (rule.threshold_price <= market_item["price"] and "Above" in rule.name)
                        ):
                            alert_message = f"{rule.name}: Current Price {market_item['price']}"
                            publish_threshold_alert(rule.symbol, alert_message)

    asyncio.run(async_task())
