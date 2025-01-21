import pika
import asyncio
import json
import logging
import time
import sys
import os
from app.resources.alerts.alert_service import process_create_alert
from app.resources.alert_rules.alert_rule_service import process_get_alert_rule_by_symbol
from app.utils.config import settings
from app.db.database import async_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RabbitMQ Subscriber")

RABBITMQ_HOST = settings.rabbitmq_host
RABBITMQ_USER = settings.rabbitmq_user
RABBITMQ_PASSWORD = settings.rabbitmq_password
EXCHANGE_NAME = "alerts_exchange"
QUEUE_NAME = "threshold_alerts_queue"
ROUTING_KEY = "alerts.*"

def init_subscriber():

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="topic", durable=True)
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=ROUTING_KEY)

    return channel

def on_event(ch, method, properties, body):
    try:
        message = json.loads(body)
        logger.info(f"Received message: {message}")

        if message.get("eventName") == "THRESHOLD_ALERT":
            symbol = message["eventData"].get("symbol")
            alert_message = message["eventData"].get("alert_message")
            status = message["eventData"].get("status")
            priority = message["eventData"].get("priority")

            if symbol and alert_message:
                logger.info(f"Processing alert for symbol: {symbol}, alert_message: {alert_message}")
                process_alert_event(symbol, alert_message, status, priority)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)

def process_alert_event(symbol: str, alert_message: str, status: str, priority: str):
    """Process the THRESHOLD_ALERT event and create a new alert record."""

    async def async_process():
        async with async_session() as db:
            alert_rule = await process_get_alert_rule_by_symbol(db, symbol)
            await process_create_alert(db, symbol, alert_message, status, priority, alert_rule.id)
            logger.info(f"Alert created for symbol: {symbol}, alert_message: {alert_message}")

    asyncio.run(async_process())

if __name__ == "__main__":
    logger.info("Starting RabbitMQ Subscriber...")
    channel = init_subscriber()

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_event)
    channel.start_consuming()
