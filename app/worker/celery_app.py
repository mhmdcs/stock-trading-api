from celery import Celery
import os
from app.utils.config import settings

RABBITMQ_HOST = settings.rabbitmq_host
RABBITMQ_USER = settings.rabbitmq_user
RABBITMQ_PASSWORD = settings.rabbitmq_password

CELERY_BROKER_URL = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@{RABBITMQ_HOST}:5672//"
CELERY_RESULT_BACKEND = "rpc://"

celery = Celery("tasks", broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

celery.autodiscover_tasks(["app.worker"])
