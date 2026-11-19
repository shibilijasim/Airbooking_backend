from django.urls import path
from .views import BookingListCreateView, CancelBookingView, DeleteBookingView

urlpatterns = [
    path('bookings/', BookingListCreateView.as_view(), name='booking_list_create'),
    path('bookings/<int:pk>/', DeleteBookingView.as_view(), name='booking_delete'),
    path('bookings/<int:pk>/cancel/', CancelBookingView.as_view(), name='booking_cancel'),
]