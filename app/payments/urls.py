from django.urls import path
from .views import KASSA24PaymentView, KaspiPaymentView, HalykPaymentView

urlpatterns = [
    path("kassa24/", KASSA24PaymentView.as_view(), name="kassa24-payment"),
    path("kaspi/", KaspiPaymentView.as_view(), name="kaspi-payment"),
    path("halyk/", HalykPaymentView.as_view(), name="halyk-payment"),
]
