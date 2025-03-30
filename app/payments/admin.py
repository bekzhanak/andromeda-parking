from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(PaymentAttempt)
admin.site.register(PaymentAttemptDebt)
admin.site.register(Payment)
admin.site.register(PaymentApplication)
