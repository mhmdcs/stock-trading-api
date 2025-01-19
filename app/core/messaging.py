import os
import json
import logging
from amqpstorm import Connection, Message
from dotenv import load_dotenv
from uuid import UUID
import uuid

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RabbitMQ Publisher")

# RabbitMQ configuration
RABBITMQ_HOST = "localhost"
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"
EXCHANGE_NAME = "alerts_exchange"
ROUTING_KEY = "alerts.threshold"

def publish_threshold_alert(symbol: str, rule_id: UUID):
    """Publish a THRESHOLD_ALERT event to RabbitMQ."""
    connection = None
    try:
        # Establish a connection
        connection = Connection(RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD)
        channel = connection.channel()

        # Declare the exchange
        channel.exchange.declare(exchange=EXCHANGE_NAME, exchange_type="topic", durable=True)

        # Prepare the message
        message_body = {
            "eventName": "THRESHOLD_ALERT",
            "eventData": {"symbol": symbol, "rule_id": rule_id},
        }
        message = Message.create(channel, json.dumps(message_body))
        message.content_type = "application/json"

        # Publish the message
        message.publish(exchange=EXCHANGE_NAME, routing_key=ROUTING_KEY)
        logger.info(f"Published message: {message_body}")
    except Exception as e:
        logger.error(f"Failed to publish message: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    # Example usage: Publish a test alert
    publish_threshold_alert(symbol="AAPL", rule_id=uuid.uuid4)
