from .models import ParkingSessionModel


class ParkingService:
    @staticmethod
    def get_total_debts(license_plate: str):
        debts = ParkingSessionModel.objects.filter(
            license_plate=license_plate,
            is_paid=False
        )

        return debts
