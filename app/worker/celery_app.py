from app.worker.async_celery import AsyncCelery
from celery.schedules import crontab
from app.utils.config import settings

RABBITMQ_HOST = settings.rabbitmq_host
RABBITMQ_USER = settings.rabbitmq_user
RABBITMQ_PASSWORD = settings.rabbitmq_password

CELERY_BROKER_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:5672//"

# Celery instance for both the celery worker and celery beat scheduler
celery = AsyncCelery("tasks", broker=CELERY_BROKER_URL)

celery.conf.include = ['app.worker.celery_task']

celery.conf.update(
    timezone="Asia/Riyadh",
    broker_connection_retry_on_startup=True,
)

celery.conf.beat_schedule = {
    "fetch-market-data-every-5-minutes": {
        "task": "app.worker.celery_task.fetch_and_check_market_data",
        "schedule": crontab(minute="*/5")
    }
}

