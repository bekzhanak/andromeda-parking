from django.db import models
from django.utils import timezone
from django.contrib.contenttypes.models import ContentType
from decimal import Decimal
from payments.models import PaymentApplication

# Create your models here.


class AbstractDebtModel(models.Model):
    """
    Abstract base model for any item that can incur debt (e.g., parking, fines).
    """
    license_plate = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0))
    created_at = models.DateTimeField(default=timezone.now)
    is_paid = models.BooleanField(default=False)

    class Meta:
        abstract = True


class ParkingSessionModel(AbstractDebtModel):
    """Represents a user's parking session with dynamic duration and price calculation."""
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def duration_minutes(self):
        end = self.end_time or timezone.now()
        return int((end - self.start_time).total_seconds() / 60)

    def get_applied_amount(self):
        ct = ContentType.objects.get_for_model(self)
        return PaymentApplication.objects.filter(
            content_type=ct,
            object_id=self.id
        ).aggregate(total=models.Sum('amount_applied'))['total'] or Decimal('0')

    def calculate_total_price(self):
        minutes = self.duration_minutes()
        base_tariff = Tariff.objects.filter(is_daily=False).order_by('-duration_minutes').first()
        max_limit = base_tariff.duration_minutes if base_tariff else 0

        if minutes <= max_limit:
            matching_tariff = Tariff.objects.filter(duration_minutes__gte=minutes, is_daily=False).order_by(
                'duration_minutes').first()
            if matching_tariff:
                return Decimal(matching_tariff.price)

        # After exceeding highest tier, charge per day (even for partial days)
        # TODO check this moment
        daily_tariff = Tariff.objects.filter(is_daily=True).first()
        if daily_tariff:
            extra_minutes = minutes - max_limit
            extra_days = (extra_minutes // 1440) + (1 if extra_minutes % 1440 > 0 else 0)
            return Decimal(daily_tariff.price) * extra_days

        return Decimal('0')

    def calculate_due_amount(self):
        total_price = self.calculate_total_price()
        applied = self.get_applied_amount()
        return max(total_price - applied, Decimal('0'))

    def update_amount(self):
        self.amount = self.calculate_total_price()
        self.save()


class Tariff(models.Model):
    """Represents a pricing tier for parking based on duration or flat daily rate."""
    duration_minutes = models.PositiveIntegerField(help_text="Max duration this tier covers")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_daily = models.BooleanField(default=False, help_text="Flat daily fee after max tier")

    class Meta:
        ordering = ['duration_minutes']

    def __str__(self):
        return f"{'Daily' if self.is_daily else f'<= {self.duration_minutes} min'}: {self.price}₸"
