import asyncio
import os
import json
from aio_pika import connect_robust, ExchangeType
from resources.alerts.alert_service import process_create_alert
from db.database import async_session

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
RABBITMQ_USER = os.getenv("RABBITMQ_USER", "guest")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD", "guest")
EXCHANGE_NAME = "alerts_exchange"
QUEUE_NAME = "threshold_alerts_queue"
ROUTING_KEY = "alerts.*"

async def process_alert_event(symbol: str, alert_message: str):
    """Process the THRESHOLD_ALERT event and create a new alert record"""
    async with async_session() as db:
        await process_create_alert(db, symbol, alert_message)
        print(f"Alert created for symbol: {symbol}, alert_message: {alert_message}")

async def handle_message(message):
    async with message.process():
        try:
            body = json.loads(message.body)

            if body.get("eventName") == "THRESHOLD_ALERT":
                symbol = body["eventData"].get("symbol")
                alert_message = body["eventData"].get("alert_message")

                if symbol and alert_message:
                    await process_alert_event(symbol, alert_message)
        except Exception as e:
            print(f"Error processing message: {e}")

async def main():
    connection = await connect_robust(f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}/")

    async with connection:
        channel = await connection.channel()

        exchange = await channel.declare_exchange(EXCHANGE_NAME, ExchangeType.TOPIC, durable=True)

        queue = await channel.declare_queue(QUEUE_NAME, durable=True)

        await queue.bind(exchange, ROUTING_KEY)

        print("listening for THRESHOLD_ALERT events to consume...")

        await queue.consume(handle_message)

if __name__ == "__main__":
    asyncio.run(main())
