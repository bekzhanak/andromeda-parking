from celery import shared_task
from .models import TaxiWhitelist
from django.utils import timezone
from datetime import timedelta


@shared_task
def delete_taxi_whitelist():
    """
    This task will delete taxi whitelist entries that are older than 30 minutes.
    """
    now = timezone.now()
    threshold_time = now - timedelta(minutes=30)

    TaxiWhitelist.objects.filter(created_at__lt=threshold_time).delete()
