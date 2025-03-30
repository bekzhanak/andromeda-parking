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
        "001AAA01", "002AAA01", "003AAA01",
        "004AAA01", "005AAA01", "006AAA01",
        "007AAA01", "008AAA01", "009AAA01",
        "010AAA01", "011AAA01", "012AAA01",
        "013AAA01", "014AAA01", "015AAA01",
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
