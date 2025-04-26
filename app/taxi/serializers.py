from rest_framework import serializers
from parking.models import ParkingArea


class YaTaxiCarSerializer(serializers.Serializer):
    """
    Serializer for the car details, including number, color, mark, model, and year.
    """
    number = serializers.CharField(max_length=20)
    color = serializers.CharField(max_length=20)
    mark = serializers.CharField(max_length=50)
    model = serializers.CharField(max_length=50)
    year = serializers.IntegerField()


class YaTaxiOrderInfoSerializer(serializers.Serializer):
    """
    Serializer for the order information, including parking id, driver details, car details, etc.
    """
    id = serializers.CharField(max_length=100)
    order_id = serializers.CharField(max_length=100)
    driver_id = serializers.CharField(max_length=100)
    arrival_time = serializers.DateTimeField()
    arrival_reason = serializers.ChoiceField(choices=["pick_up", "drop"])
    polygon_id = serializers.PrimaryKeyRelatedField(queryset=ParkingArea.objects.all())

    car = YaTaxiCarSerializer()

    order_class = serializers.CharField(max_length=100)  # Order class (e.g., tariff)
