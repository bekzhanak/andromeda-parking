import os
import django
from datetime import timedelta
from decimal import Decimal
from django.utils import timezone

# ✅ Set up Django environment (replace with your project name)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")  # ← CHANGE THIS
django.setup()

from parking.models import ParkingSessionModel


def generate_kassa24_test_data():
    plates = [
        "101AAA01", "102AAA01", "103AAA01",
        "104AAA01", "105AAA01", "106AAA01",
        "107AAA01", "108AAA01", "109AAA01",
        "110AAA01", "111AAA01", "112AAA01",
        "113AAA01", "114AAA01", "115AAA01",
    ]

    # Delete any existing test data
    ParkingSessionModel.objects.filter(license_plate__in=plates).delete()

    # Create new sessions
    for plate in plates:
        session = ParkingSessionModel.objects.create(
            license_plate=plate,
            start_time=timezone.now() - timedelta(hours=2, minutes=30),
            is_active=True,
        )
        session.update_amount()

    print(f"✅ Test parking sessions created for {len(plates)} license plates.")


if __name__ == "__main__":
    generate_kassa24_test_data()
