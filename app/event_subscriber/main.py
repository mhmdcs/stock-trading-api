import os
import json
import logging
import pika
import asyncio
from dotenv import load_dotenv
from resources.alerts.alert_service import process_create_alert
from db.database import async_session
from uuid import UUID

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RabbitMQ Subscriber")

# RabbitMQ configuration
RABBITMQ_HOST = "localhost"
EXCHANGE_NAME = "alerts_exchange"
QUEUE_NAME = "threshold_alerts_queue"
ROUTING_KEY = "alerts.*"

def init_subscriber():
    """Initialize the RabbitMQ subscriber connection."""
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    # Declare the exchange
    channel.exchange_declare(exchange=EXCHANGE_NAME, exchange_type="topic", durable=True)

    # Declare the queue
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Bind the queue to the exchange with the routing key
    channel.queue_bind(exchange=EXCHANGE_NAME, queue=QUEUE_NAME, routing_key=ROUTING_KEY)

    return connection, channel

def on_event(ch, method, properties, body):
    """Handle incoming RabbitMQ messages."""
    try:
        # Parse the message
        message = json.loads(body)
        logger.info(f"Received message: {message}")

        # Process the THRESHOLD_ALERT event
        if message.get("eventName") == "THRESHOLD_ALERT":
            symbol = message["eventData"].get("symbol")
            rule_id = message["eventData"].get("rule_id")

            if symbol and rule_id:
                logger.info(f"Processing alert for symbol: {symbol}, rule_id: {rule_id}")
                process_alert_event(symbol, rule_id)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)


def process_alert_event(symbol: str, rule_id: UUID):
    """Process the THRESHOLD_ALERT event."""
    async def async_process_alert():
        """Asynchronous wrapper to handle alert creation."""
        async with async_session() as db:
            await process_create_alert(db, symbol, rule_id)
            logger.info(f"Alert created for symbol: {symbol}, rule_id: {rule_id}")

    # Get the current event loop
    loop = asyncio.get_event_loop()

    # Schedule the async function to run on the existing loop
    loop.create_task(async_process_alert())

if __name__ == "__main__":
    logger.info("Starting RabbitMQ Subscriber...")
    connection, channel = init_subscriber()

    # Start consuming messages
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_event)
    try:
        logger.info("Listening for THRESHOLD_ALERT events...")
        channel.start_consuming()
    except KeyboardInterrupt:
        logger.info("Stopping RabbitMQ Subscriber...")
        channel.stop_consuming()
    finally:
        connection.close()
