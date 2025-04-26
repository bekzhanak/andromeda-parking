import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

app = Celery('backend')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'delete-taxi-whitelist-every-10-minutes': {
        'task': 'taxi.tasks.delete_taxi_whitelist',
        'schedule': crontab(minute='*/10'),  # Run every 10 minutes
    },
}
