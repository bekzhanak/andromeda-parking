from django.urls import path
from .views import YaTaxiInfoOrderOutView


urlpatterns = [
    path("ya_taxi/info_order_out/", YaTaxiInfoOrderOutView.as_view(), name="ya_taxi_info_order_out"),
]
