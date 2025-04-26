from django.db import models
from django.utils import timezone
from parking.models import ParkingArea


class TaxiArrivalReason(models.TextChoices):
    PICK_UP = "pick_up", "Pick Up"
    DROP = "drop", "Drop"


class TaxiWhitelist(models.Model):
    license_plate = models.CharField(max_length=20)
    created_at = models.DateTimeField(default=timezone.now)
    parking_area = models.ForeignKey(ParkingArea, on_delete=models.CASCADE)
    arrival_reason = models.CharField(
        max_length=20,
        choices=TaxiArrivalReason.choices,
    )

    def __str__(self):
        return f"Taxi {self.license_plate} whitelisted for {self.parking_area.name}"
