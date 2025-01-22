from celery import Celery
from celery.schedules import crontab
from app.utils.config import settings

RABBITMQ_HOST = settings.rabbitmq_host
RABBITMQ_USER = settings.rabbitmq_user
RABBITMQ_PASSWORD = settings.rabbitmq_password

CELERY_BROKER_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:5672//"
CELERY_RESULT_BACKEND = "rpc://"

# Celery instance for both the celery worker and celery beat scheduler
celery = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

celery.conf.include = ['app.worker.celery_task']

celery.conf.beat_schedule = {
    "fetch-market-data-every-5-minutes": {
        "task": "app.worker.celery_task.fetch_and_check_market_data",
        "schedule": crontab(minute="*/5")
    }
}

celery.conf.timezone = "Asia/Riyadh"
