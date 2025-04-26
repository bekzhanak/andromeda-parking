from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(ParkingSessionModel)
admin.site.register(Tariff)


# Inline admin for CameraConfiguration under ParkingArea
class CameraConfigurationInline(admin.TabularInline):
    """Inline to manage cameras under parking area."""
    model = CameraConfiguration
    extra = 1  # Number of empty camera rows to display by default in the form
    fields = ('camera_name', 'direction', 'parking_area')


# Admin for ParkingArea, with CameraConfiguration inline
class ParkingAreaAdmin(admin.ModelAdmin):
    """Admin view for ParkingArea, with inline CameraConfiguration."""
    inlines = [CameraConfigurationInline]
    list_display = ('name',)  # Customize this as needed


# Inline admin for CarImage under ParkingEvent
class CarImageInline(admin.TabularInline):
    """Inline to manage car images under parking event."""
    model = CarImage
    extra = 1  # Number of empty image rows to display by default in the form
    fields = ('license_plate', 'car_image', 'captured_at', 'camera_configuration')


# Admin for ParkingEvent, with CarImage inline
class ParkingEventAdmin(admin.ModelAdmin):
    """Admin view for ParkingEvent, with inline CarImage."""
    inlines = [CarImageInline]
    list_display = ('parking_session', 'event_type', 'event_time')  # Customize this as needed


# Register the new models in the admin
admin.site.register(ParkingArea, ParkingAreaAdmin)
admin.site.register(ParkingEvent, ParkingEventAdmin)
admin.site.register(TaxiEvent)
