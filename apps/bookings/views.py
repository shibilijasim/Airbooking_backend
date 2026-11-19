from decimal import Decimal
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Booking
from .serializers import BookingSerializer

class BookingListCreateView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookingSerializer

    def get_queryset(self):
        return Booking.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CancelBookingView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

        if booking.status == 'Cancelled':
            return Response({"error": "This booking is already cancelled."}, status=status.HTTP_400_BAD_REQUEST)

        passenger_index = request.data.get('passenger_index', None)
        passengers = list(booking.passengers or [])

        # Group cancellation
        if passenger_index is None:
            for p in passengers:
                p['status'] = 'Cancelled'
            booking.passengers = passengers
            booking.ticket_count = 0
            booking.total_price = Decimal('0.00')
            booking.status = 'Cancelled'
            booking.save()
            return Response(BookingSerializer(booking).data, status=status.HTTP_200_OK)

        # Individual passenger cancellation
        try:
            idx = int(passenger_index)
            if idx < 0 or idx >= len(passengers):
                raise ValueError
        except (TypeError, ValueError):
            return Response({"error": "Invalid passenger index."}, status=status.HTTP_400_BAD_REQUEST)

        if passengers[idx].get('status') == 'Cancelled':
            return Response({"error": "This passenger's ticket is already cancelled."}, status=status.HTTP_400_BAD_REQUEST)

        active_count_before = sum(1 for p in passengers if p.get('status') != 'Cancelled')
        unit_price = (booking.total_price / Decimal(active_count_before)) if active_count_before > 0 else Decimal('0.00')

        passengers[idx]['status'] = 'Cancelled'
        active_count_after = active_count_before - 1

        booking.passengers = passengers
        booking.ticket_count = active_count_after
        booking.total_price = max(Decimal('0.00'), (booking.total_price - unit_price).quantize(Decimal('0.01')))

        if active_count_after == 0:
            booking.status = 'Cancelled'

        booking.save()
        return Response(BookingSerializer(booking).data, status=status.HTTP_200_OK)


class DeleteBookingView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, user=request.user)
        except Booking.DoesNotExist:
            return Response({"error": "Booking not found."}, status=status.HTTP_404_NOT_FOUND)

        if booking.status != 'Cancelled':
            return Response(
                {"error": "Only cancelled trips can be deleted."},
                status=status.HTTP_400_BAD_REQUEST
            )

        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)