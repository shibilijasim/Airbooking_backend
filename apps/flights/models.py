from django.db import models


class Flight(models.Model):
    STATUS_CHOICES = [
        ('On-Time', 'On-Time'),
        ('Scheduled', 'Scheduled'),
        ('Delayed', 'Delayed'),
        ('Boarding', 'Boarding'),
        ('Cancelled', 'Cancelled'),
        ('Landed', 'Landed'),
    ]

    flight_number = models.CharField(max_length=20)
    departure_airport = models.CharField(max_length=10)
    arrival_airport = models.CharField(max_length=10)
    departure_time = models.CharField(max_length=50)
    travel_hours = models.DecimalField(max_digits=5, decimal_places=2, default=2.0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=100.00)
    available_seats = models.PositiveIntegerField(default=18)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='On-Time')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.flight_number} ({self.departure_airport} -> {self.arrival_airport})"