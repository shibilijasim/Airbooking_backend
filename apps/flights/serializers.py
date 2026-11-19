from rest_framework import serializers
from .models import Flight


class FlightSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = [
            'id',
            'flight_number',
            'departure_airport',
            'arrival_airport',
            'departure_time',
            'travel_hours',
            'price',
            'available_seats',
            'status',
            'updated_at',
        ]
        read_only_fields = ['id', 'updated_at']


class FlightStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = ['status']