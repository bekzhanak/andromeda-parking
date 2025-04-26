from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied
from .serializers import *
from .services import TaxiService
from django.conf import settings


class YaTaxiInfoOrderOutView(APIView):
    """
    View used by YaTaxi to notify the service when the order to our area is created.
    """
    def post(self, request: Request) -> Response:
        ya_taxi_key = request.headers.get("Authorization")

        if not ya_taxi_key or ya_taxi_key.split()[1] != settings.YA_TAXI_KEY:
            raise PermissionDenied()

        serializer = YaTaxiOrderInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        taxi_data = serializer.validated_data
        TaxiService.add_to_whitelist(taxi_data)
        return Response({"message": "ok"})
