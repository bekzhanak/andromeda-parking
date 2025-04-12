from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from .serializers import ParkingEventSerializer
from .models import *
from backend.settings import CV_API_KEY
from rest_framework.exceptions import PermissionDenied


class ParkingEventView(APIView):
    """
    API view to handle parking events.
    """

    def post(self, request: Request) -> Response:
        api_key = request.headers.get("Authorization")

        if api_key.split()[1] != CV_API_KEY:
            raise PermissionDenied()

        serializer = ParkingEventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        license_plate = serializer.validated_data["license_plate_text"]
        car_image = serializer.validated_data["car_image"]

        camera = CameraConfiguration.objects.get(camera_name=serializer.validated_data['camera_name'])
        if camera.direction == CameraConfiguration.IN:

            parking_session = ParkingSessionModel.objects.create(
                license_plate=license_plate,
                parking_area=camera.parking_area
            )

            parking_event = ParkingEvent.objects.create(
                parking_session=parking_session,
                event_type=CameraConfiguration.IN
            )

            CarImage.objects.create(
                license_plate=license_plate,
                car_image=car_image,
                camera_configuration=camera,
                parking_event=parking_event
            )

            # TODO shlagbaum opening logic here

            return Response({"message": "Parking event recorded successfully."}, status=201)

        elif camera.direction == CameraConfiguration.OUT:
            debts = ParkingSessionModel.objects.filter(
                license_plate=license_plate,
                is_paid=False
            )

            total_due = sum([debt.calculate_due_amount() for debt in debts])

            if not total_due:
                last_parking_session = debts.last()

                if debts:
                    parking_event = ParkingEvent.objects.create(
                        parking_session=last_parking_session,
                        event_type=CameraConfiguration.OUT
                    )

                    CarImage.objects.create(
                        license_plate=license_plate,
                        car_image=car_image,
                        camera_configuration=camera,
                        parking_event=parking_event
                    )

                for debt in debts:
                    debt.is_paid = True
                    debt.is_active = False
                    debt.save(update_fields=["is_active", "is_paid"])

                # TODO shlagbaum opening logic here

                return Response({"message": "Parking event recorded successfully."}, status=201)

        return Response(status=status.HTTP_400_BAD_REQUEST)

