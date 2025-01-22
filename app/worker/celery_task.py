from app.worker.celery_app import celery
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
                        print(f"fetched data for {rule.symbol} - rule threshold price is {rule.threshold_price} - current market price is {market_item["price"]}")
                        if (
                            (market_item["price"] <= rule.threshold_price and "Below" in rule.name)
                            or (market_item["price"] >= rule.threshold_price and "Above" in rule.name)
                        ):
                            alert_message = f"{rule.name}: Current Price {market_item['price']}"
                            print(f"publishing alert notification: {alert_message}")
                            publish_threshold_alert(symbol=rule.symbol, alert_message=alert_message, status="recent", priority="medium")

    asyncio.run(async_task())
