from django.db import models

class Flight(models.Model):
    STATUS_CHOICES = (
        ('On-time', 'On-time'),
        ('Delayed', 'Delayed'),
    )
    flight_number = models.CharField(max_length=50, unique=True)
    departure_airport = models.CharField(max_length=100)
    arrival_airport = models.CharField(max_length=100)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    available_seats = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='On-time')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    travel_hours = models.DecimalField(max_digits=4, decimal_places=2, default=0.00)

    def __str__(self):
        return f"{self.flight_number}: {self.departure_airport} to {self.arrival_airport}"