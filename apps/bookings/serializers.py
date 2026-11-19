# from rest_framework import serializers
# from .models import Booking
# from apps.flights.serializers import FlightSerializer

# class BookingSerializer(serializers.ModelSerializer):
#     # Optional: Include flight details when fetching bookings for "My Trips"
#     flight_details = FlightSerializer(source='flight', read_only=True)

#     class Meta:
#         model = Booking
#         fields = ('id', 'user', 'flight', 'flight_details', 'seats_reserved', 'payment_status', 'created_at')
#         read_only_fields = ('user', 'payment_status')

#     def validate(self, data):
#         flight = data['flight']
#         seats_requested = data.get('seats_reserved', 1)
        
#         if flight.available_seats < seats_requested:
#             raise serializers.ValidationError("Not enough available seats on this flight.")
#         return data




from rest_framework import serializers
from .models import Booking

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user', 'status', 'booked_at']