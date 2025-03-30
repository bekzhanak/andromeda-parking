from django.urls import path
from .views import KASSA24PaymentView


urlpatterns = [
    path("kassa24/", KASSA24PaymentView.as_view(), name="kassa24-payment"),
]
