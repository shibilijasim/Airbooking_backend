# from django.urls import path
# from .views import BookingListCreateView, BookingDetailView

# urlpatterns = [
#     # Booking Management
#     path('bookings/', BookingListCreateView.as_view(), name='bookings_list_create'),
#     path('bookings/<int:id>/', BookingDetailView.as_view(), name='booking_detail'),
# ]

# from django.urls import path
# from .views import BookingListCreateView, CancelBookingView

# urlpatterns = [
#     path('bookings/', BookingListCreateView.as_view(), name='booking_list_create'),
#     path('bookings/<int:pk>/cancel/', CancelBookingView.as_view(), name='booking_cancel'),
# ]



from django.urls import path
from .views import BookingListCreateView, CancelBookingView, DeleteBookingView

urlpatterns = [
    path('bookings/', BookingListCreateView.as_view(), name='booking_list_create'),
    path('bookings/<int:pk>/', DeleteBookingView.as_view(), name='booking_delete'),
    path('bookings/<int:pk>/cancel/', CancelBookingView.as_view(), name='booking_cancel'),
]