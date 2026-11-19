import requests
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Flight
from .serializers import FlightSerializer

# --- 1. Database Flight Search (Legacy/Optional) ---
class FlightSearchView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    serializer_class = FlightSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Flight.objects.all()
        
        departure = self.request.query_params.get('departure')
        arrival = self.request.query_params.get('arrival')
        if departure:
            queryset = queryset.filter(departure_airport__icontains=departure)
        if arrival:
            queryset = queryset.filter(arrival_airport__icontains=arrival)
            
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        max_hours = self.request.query_params.get('max_hours')
        
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        if max_hours:
            queryset = queryset.filter(travel_hours__lte=max_hours)

        sort_by = self.request.query_params.get('sort_by')
        sort_order = self.request.query_params.get('sort_order')
        
        if sort_by in ['price', 'travel_hours']:
            prefix = '-' if sort_order == 'desc' else ''
            queryset = queryset.order_by(f'{prefix}{sort_by}')
            
        return queryset

# --- 2. Database Flight Detail ---
class FlightDetailView(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'id'

# --- 3. Admin Flight Management ---
class AdminFlightListView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [permissions.IsAdminUser]

class AdminFlightStatusUpdateView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [permissions.IsAdminUser]
    lookup_field = 'id'

# --- 4. Live Radar Tracking (AirLabs Proxy) ---
class LiveFlightTrackingView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, flight_iata):
        airlabs_api_key = '7b99c8c6-e786-4557-a7c3-82d44aadb2fe' 
        
        url = f"https://airlabs.co/api/v9/flight?flight_iata={flight_iata}&api_key={airlabs_api_key}"
        
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            
            if 'response' in data:
                live = data['response']
                return Response({
                    "flight_number": live.get("flight_iata", flight_iata),
                    "departure_airport": live.get("dep_iata", "N/A"),
                    "arrival_airport": live.get("arr_iata", "N/A"),
                    "status": live.get("status", "Unknown"),
                    "altitude_meters": live.get("alt", 0),
                    "speed_kmh": live.get("speed", 0),
                    "delayed": live.get("delayed", 0),
                    "lat": live.get("lat", 0),
                    "lng": live.get("lng", 0)
                })
            elif 'error' in data:
                error_msg = data['error'].get('message', 'Unknown AirLabs Error')
                return Response(
                    {"error": f"AirLabs: {error_msg}"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                return Response(
                    {"error": "Flight not found on radar. It may be grounded."}, 
                    status=status.HTTP_404_NOT_FOUND
                )
                
        except requests.RequestException:
            return Response(
                {"error": "Failed to connect to AirLabs radar servers."}, 
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

# --- 5. Live Schedule Search with Filters & Sorting (AirLabs Proxy) ---
class LiveFlightSearchView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        airlabs_api_key = '7b99c8c6-e786-4557-a7c3-82d44aadb2fe' 
        
        dep = request.query_params.get('departure', '').upper().strip()
        arr = request.query_params.get('arrival', '').upper().strip()
        
        if not dep and not arr:
            return Response(
                {"error": "Please enter at least a Departure or Arrival airport IATA code (e.g., JFK, LAX)."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        url = f"https://airlabs.co/api/v9/schedules?api_key={airlabs_api_key}"
        if dep: url += f"&dep_iata={dep}"
        if arr: url += f"&arr_iata={arr}"
        
        try:
            res = requests.get(url, timeout=10)
            data = res.json()
            
            if 'error' in data:
                return Response({"error": data['error'].get('message', 'AirLabs error')}, status=status.HTTP_400_BAD_REQUEST)
                
            schedules = data.get('response', [])
            processed_flights = []
            
            for s in schedules:
                flight_num = s.get('flight_iata') or s.get('flight_icao')
                if not flight_num:
                    continue
                    
                base_price = sum(ord(c) for c in flight_num) % 400 + 150 
                
                duration_mins = s.get('duration', 0)
                if not duration_mins:
                    duration_mins = (base_price % 300) + 60 
                travel_hours = round(duration_mins / 60, 2)
                
                processed_flights.append({
                    "flight_number": flight_num,
                    "departure_airport": s.get('dep_iata', dep),
                    "arrival_airport": s.get('arr_iata', arr),
                    "departure_time": s.get('dep_time_utc', 'Scheduled'),
                    "status": s.get('status', 'scheduled'),
                    "price": float(base_price),
                    "travel_hours": float(travel_hours)
                })
                
            min_price = float(request.query_params.get('min_price') or 0)
            max_price = float(request.query_params.get('max_price') or 99999)
            max_hours = float(request.query_params.get('max_hours') or 999)
            
            filtered_flights = [
                f for f in processed_flights
                if min_price <= f['price'] <= max_price
                and f['travel_hours'] <= max_hours
            ]
            
            sort_by = request.query_params.get('sort_by', 'price')
            sort_order = request.query_params.get('sort_order', 'asc')
            reverse_order = (sort_order == 'desc')
            
            if sort_by in ['price', 'travel_hours']:
                filtered_flights.sort(key=lambda x: x[sort_by], reverse=reverse_order)
                
            return Response(filtered_flights[:50])
            
        except Exception as e:
            return Response({"error": "Failed to fetch live schedules from AirLabs."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)