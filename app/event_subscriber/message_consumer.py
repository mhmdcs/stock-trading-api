import pika
import json
from asgiref.sync import async_to_sync
from app.resources.alerts.alert_service import process_create_alert
from app.utils.config import settings
from app.db.database import async_session

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
        print(f"RabbitMQ Subscriber: Received message: {message}")

        if message.get("eventName") == "THRESHOLD_ALERT":
            symbol = message["eventData"].get("symbol")
            alert_message = message["eventData"].get("alert_message")
            status = message["eventData"].get("status")
            priority = message["eventData"].get("priority")

            if symbol and alert_message and status and priority:
                print(f"RabbitMQ Subscriber: Processing alert for symbol: {symbol}, alert_message: {alert_message}")
                async_to_sync(process_alert_event)(symbol, alert_message, status, priority)
    except Exception as e:
        print(f"RabbitMQ Subscriber: Error processing message: {e}")
    finally:
        ch.basic_ack(delivery_tag=method.delivery_tag)

async def process_alert_event(symbol: str, alert_message: str, status: str, priority: str):
    """Process the THRESHOLD_ALERT event and create a new alert record."""
    async with async_session() as db:
        await process_create_alert(db, symbol, alert_message, status, priority)
        print(f"RabbitMQ Subscriber: Alert created for symbol: {symbol}, alert_message: {alert_message}")


if __name__ == "__main__":
    channel = init_subscriber()

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=on_event)
    channel.start_consuming()
