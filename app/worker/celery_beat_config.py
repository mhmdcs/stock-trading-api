from celery import Celery
from celery.schedules import crontab

celery = Celery()

celery.conf.beat_schedule = {
    "fetch-market-data-every-5-minutes": {
        "task": "app.tasks.fetch_and_check_market_data",
        "schedule": crontab(minute="*/5"),
    }
}

celery.conf.timezone = "UTC"
