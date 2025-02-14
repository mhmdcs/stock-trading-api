from amqpstorm import Connection, Message
import json
from app.utils.config import settings

RABBITMQ_HOST = settings.rabbitmq_host
RABBITMQ_USER = settings.rabbitmq_user
RABBITMQ_PASSWORD = settings.rabbitmq_password
EXCHANGE_NAME = "alerts_exchange"
ROUTING_KEY = "alerts.threshold"


def publish_threshold_alert(symbol: str, alert_message: str, status: str, priority: str):
    """Publish a THRESHOLD_ALERT event to RabbitMQ queue"""
    connection = None
    try:

        connection = Connection(RABBITMQ_HOST, RABBITMQ_USER, RABBITMQ_PASSWORD)
        channel = connection.channel()

        channel.exchange.declare(exchange=EXCHANGE_NAME, exchange_type="topic", durable=True)

        message_content = {
            "eventName": "THRESHOLD_ALERT",
            "eventData": {"symbol": symbol, "alert_message": alert_message, "status": status, "priority": priority},
        }
        message = Message.create(channel, json.dumps(message_content))
        message.content_type = "application/json"

        message.publish(exchange=EXCHANGE_NAME, routing_key=ROUTING_KEY)
        print(f"RabbitMQ Publisher: Published message: {message_content}")
    except Exception as e:
        print(f"RabbitMQ Publisher: Failed to publish message: {e}")
    finally:
        if connection:
            connection.close()

if __name__ == "__main__":
    # publish a test alert
    publish_threshold_alert(symbol="AAPL", alert_message="Apple Above $200", status="now", priority="high")
