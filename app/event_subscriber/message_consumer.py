import pika
import asyncio
import json
import logging
import time
import sys
import os

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(project_root)
from app.resources.alerts.alert_service import process_create_alert
from app.resources.alert_rules.alert_rule_service import process_get_alert_rule_by_symbol
from app.db.database import async_session

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RabbitMQ Subscriber")

RABBITMQ_HOST = "localhost"
EXCHANGE_NAME = "alerts_exchange"
QUEUE_NAME = "threshold_alerts_queue"
ROUTING_KEY = "alerts.*"

# wait for rabbitmq broker to be initialized first via docker compose
def wait_for_rabbitmq():
    while True:
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
            connection.close()
            break
        except:
            time.sleep(5)

def init_subscriber():
    wait_for_rabbitmq()

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

            if symbol and alert_message:
                logger.info(f"Processing alert for symbol: {symbol}, alert_message: {alert_message}")
                process_alert_event(symbol, alert_message)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)

def process_alert_event(symbol: str, alert_message: str):
    """Process the THRESHOLD_ALERT event and create a new alert record."""

    async def async_process():
        async with async_session() as db:
            alert_rule = await process_get_alert_rule_by_symbol(db, symbol)
            await process_create_alert(db, symbol, alert_message, alert_rule.id)
            logger.info(f"Alert created for symbol: {symbol}, alert_message: {alert_message}")

    asyncio.run(async_process())

if __name__ == "__main__":
    logger.info("Starting RabbitMQ Subscriber...")
    channel = init_subscriber()

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_event)
    channel.start_consuming()
