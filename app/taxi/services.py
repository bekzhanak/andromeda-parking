from .models import *
from datetime import timedelta


class TaxiService:
    @staticmethod
    def add_to_whitelist(taxi_data: dict) -> None:
        """
        Adds a taxi to the whitelist.
        :param taxi_data: Dictionary containing taxi data.
        :return: None
        """
        license_plate = taxi_data.get("car", {}).get("number")
        parking_area = taxi_data.get("polygon_id")
        arrival_reason = taxi_data.get("arrival_reason")

        taxi_entry = TaxiWhitelist.objects.filter(
            license_plate=license_plate,
            parking_area=parking_area,
            arrival_reason=arrival_reason,
        ).first()

        if taxi_entry:
            taxi_entry.created_at = timezone.now()
            taxi_entry.save()
            return
        else:
            TaxiWhitelist.objects.create(
                license_plate=license_plate,
                parking_area=parking_area,
                arrival_reason=arrival_reason,
            )

    @staticmethod
    def is_whitelisted(license_plate: str, parking_area: ParkingArea) -> bool:
        """
        Checks if a taxi is whitelisted for a given parking area.
        :param license_plate: The license plate of the taxi.
        :param parking_area: The parking area to check against.
        :return: True if the taxi is whitelisted, False otherwise.
        """
        return TaxiWhitelist.objects.filter(
            license_plate=license_plate,
            parking_area=parking_area,
            created_at__gte=timezone.now() - timedelta(minutes=30)
        ).exists()
