from django.db import models
from django.conf import settings
from django.utils import timezone

class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    flight_number = models.CharField(max_length=20, default='N/A')
    departure_airport = models.CharField(max_length=10, default='N/A')
    arrival_airport = models.CharField(max_length=10, default='N/A')
    departure_time = models.CharField(max_length=50, default='Scheduled')
    travel_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    ticket_count = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    contact_email = models.EmailField(default='test@example.com')
    contact_phone = models.CharField(max_length=20, default='0000000000')
    passengers = models.JSONField(default=list)
    status = models.CharField(max_length=20, default='Confirmed')
    booked_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-booked_at']