from django.urls import path
from .views import FlightSearchView, FlightDetailView, AdminFlightListView, AdminFlightStatusUpdateView, LiveFlightSearchView, LiveFlightTrackingView

urlpatterns = [
    # Public Flight Search
    path('flights/search/', FlightSearchView.as_view(), name='flight_search'),
    path('flights/<int:id>/', FlightDetailView.as_view(), name='flight_detail'),
    path('flights/live-search/', LiveFlightSearchView.as_view(), name='live_flight_search'),
    path('flights/live/<str:flight_iata>/', LiveFlightTrackingView.as_view(), name='live_flight_tracker'),
    
    # Admin Flight Management
    path('admin/flights/', AdminFlightListView.as_view(), name='admin_flights'),
    path('admin/flights/<int:id>/status/', AdminFlightStatusUpdateView.as_view(), name='admin_flight_status'),
]