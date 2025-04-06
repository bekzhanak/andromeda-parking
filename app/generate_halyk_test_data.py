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
        "201AAA01", "202AAA01", "203AAA01",
        "204AAA01", "205AAA01", "206AAA01",
        "207AAA01", "208AAA01", "209AAA01",
        "210AAA01", "211AAA01", "212AAA01",
        "213AAA01", "214AAA01", "215AAA01",
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
