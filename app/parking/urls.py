from django.urls import path
from .views import ParkingEventView


urlpatterns = [
    path("event/", ParkingEventView.as_view(), name="parking-event")
]
