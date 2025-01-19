from amqpstorm import Connection, Message
import json
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("RabbitMQ Publisher")

RABBITMQ_HOST = "localhost"
RABBITMQ_USER = "guest"
RABBITMQ_PASSWORD = "guest"
EXCHANGE_NAME = "alerts_exchange"
ROUTING_KEY = "alerts.threshold"

def publish_threshold_alert(symbol: str, alert_message: str):
    """Publish a THRESHOLD_ALERT event to RabbitMQ queue"""
    connection = None
    try:

        connection = Connection(RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD)
        channel = connection.channel()

        channel.exchange.declare(exchange=EXCHANGE_NAME, exchange_type="topic", durable=True)

        message_content = {
            "eventName": "THRESHOLD_ALERT",
            "eventData": {"symbol": symbol, "alert_message": alert_message},
        }
        message = Message.create(channel, json.dumps(message_content))
        message.content_type = "application/json"

        message.publish(exchange=EXCHANGE_NAME, routing_key=ROUTING_KEY)
        logger.info(f"Published message: {message_content}")
    except Exception as e:
        logger.error(f"Failed to publish message: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    # publish a test alert
    publish_threshold_alert(symbol="AAPL", alert_message="Apple above $300")
