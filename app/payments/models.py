from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


class PaymentProvider(models.TextChoices):
    """Enumeration of supported payment providers."""
    KASSA24 = 'KASSA24', 'Kassa24'


class PaymentAttempt(models.Model):
    """Stores a pending or completed payment attempt generated during 'check' phase."""
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        PAID = 'PAID', 'Paid'

    license_plate = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    provider = models.CharField(max_length=30, choices=PaymentProvider.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    def __str__(self):
        return f"Attempt for {self.license_plate} - {self.amount}₸"


class PaymentAttemptDebt(models.Model):
    """Links a PaymentAttempt to a debt item via GenericForeignKey."""
    payment_attempt = models.ForeignKey(PaymentAttempt, on_delete=models.CASCADE, related_name="debts")
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    debt_object = GenericForeignKey('content_type', 'object_id')


class Payment(models.Model):
    """Represents a confirmed payment made by a user, linked to a previous attempt."""
    license_plate = models.CharField(max_length=20)
    receipt = models.CharField(max_length=50, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField()
    note = models.CharField(max_length=255, blank=True)
    provider = models.CharField(max_length=30, choices=PaymentProvider.choices)
    attempt = models.ForeignKey(PaymentAttempt, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')

    def __str__(self):
        return f"Payment {self.receipt} - {self.amount}₸"


class PaymentApplication(models.Model):
    """Links a Payment to one or more debt items and specifies how much was applied to each."""
    payment = models.ForeignKey(Payment, related_name='applications', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    debt_object = GenericForeignKey('content_type', 'object_id')

    amount_applied = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.amount_applied}₸ → {self.debt_object}"
