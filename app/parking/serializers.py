from rest_framework import serializers


class ParkingEventSerializer(serializers.Serializer):
    camera_name = serializers.CharField(max_length=255)
    license_plate_text = serializers.CharField(max_length=20)
    car_image = serializers.CharField()  # Assuming base64 image string is passed
