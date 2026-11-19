# from rest_framework import generics, permissions
# from .models import Flight
# from .serializers import FlightSerializer

# class FlightSearchView(generics.ListAPIView):
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         queryset = Flight.objects.all()
#         # Filtering capabilities
#         departure = self.request.query_params.get('departure', None)
#         arrival = self.request.query_params.get('arrival', None)
#         date = self.request.query_params.get('date', None)
        
#         if departure:
#             queryset = queryset.filter(departure_airport__icontains=departure)
#         if arrival:
#             queryset = queryset.filter(arrival_airport__icontains=arrival)
#         if date:
#             queryset = queryset.filter(departure_time__date=date)
            
#         return queryset

# class FlightDetailView(generics.RetrieveAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     lookup_field = 'id'

# # --- Admin Views ---
# class AdminFlightListView(generics.ListCreateAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAdminUser]

# class AdminFlightStatusUpdateView(generics.UpdateAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAdminUser]
#     lookup_field = 'id'



# import requests
# from rest_framework import generics, permissions
# from rest_framework.response import Response
# from .models import Flight
# from .serializers import FlightSerializer

# class FlightDetailView(generics.RetrieveAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     lookup_field = 'id'

# # --- Admin Views ---
# class AdminFlightListView(generics.ListCreateAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAdminUser]

# class FlightDetailView(generics.RetrieveAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     lookup_field = 'id'

#     def retrieve(self, request, *args, **kwargs):
#         # 1. Get standard flight data from your database
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         flight_data = serializer.data

#         # 2. Fetch real-time data from AirLabs
#         airlabs_api_key = 'YOUR_AIRLABS_API_KEY' # Replace with actual key
#         flight_iata = instance.flight_number

#         try:
#             url = f"https://airlabs.co/api/v9/flight?flight_iata={flight_iata}&api_key={airlabs_api_key}"
#             api_response = requests.get(url, timeout=5)
            
#             if api_response.status_code == 200:
#                 live_data = api_response.json().get('response', {})
#                 flight_data['live_metrics'] = {
#                     'status': live_data.get('status', instance.status),
#                     'altitude_meters': live_data.get('alt', 0),
#                     'speed_kmh': live_data.get('speed', 0),
#                     'delayed': live_data.get('delayed', 0)
#                 }
#             else:
#                 flight_data['live_metrics'] = None
#         except requests.RequestException:
#             # Fallback if external API fails
#             flight_data['live_metrics'] = None

#         return Response(flight_data)


# import requests

# from rest_framework import generics, permissions
# from rest_framework.response import Response

# from .models import Flight
# from .serializers import FlightSerializer


# # 1. Public Flight Search
# class FlightSearchView(generics.ListAPIView):
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.AllowAny]

#     def get_queryset(self):
#         queryset = Flight.objects.all()

#         source = self.request.query_params.get('source')
#         destination = self.request.query_params.get('destination')

#         if source:
#             queryset = queryset.filter(source__icontains=source)

#         if destination:
#             queryset = queryset.filter(destination__icontains=destination)

#         return queryset


# # 2. Flight Details with Live AirLabs Data
# class FlightDetailView(generics.RetrieveAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     lookup_field = 'id'

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)
#         flight_data = serializer.data

#         airlabs_api_key = '7b99c8c6-e786-4557-a7c3-82d44aadb2fe'
#         flight_iata = instance.flight_number

#         try:
#             url = (
#                 f"https://airlabs.co/api/v9/flight"
#                 f"?flight_iata={flight_iata}&api_key={airlabs_api_key}"
#             )

#             api_response = requests.get(url, timeout=5)

#             if api_response.status_code == 200:
#                 live_data = api_response.json().get('response', {})

#                 flight_data['live_metrics'] = {
#                     'status': live_data.get('status', instance.status),
#                     'altitude_meters': live_data.get('alt', 0),
#                     'speed_kmh': live_data.get('speed', 0),
#                     'delayed': live_data.get('delayed', 0)
#                 }
#             else:
#                 flight_data['live_metrics'] = None

#         except requests.RequestException:
#             flight_data['live_metrics'] = None

#         return Response(flight_data)


# # 3. Admin Flight List and Create
# class AdminFlightListView(generics.ListCreateAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAdminUser]


# # 4. Admin Flight Status Update
# class AdminFlightStatusUpdateView(generics.UpdateAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAdminUser]
#     lookup_field = 'id'


















# import requests

# from rest_framework import generics, permissions
# from rest_framework.response import Response

# from .models import Flight
# from .serializers import FlightSerializer


# # 1. Public Flight Search
# class FlightSearchView(generics.ListAPIView):
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.AllowAny]

#     def get_queryset(self):
#         queryset = Flight.objects.all()

#         source = self.request.query_params.get('source')
#         destination = self.request.query_params.get('destination')

#         if source:
#             queryset = queryset.filter(source__icontains=source)

#         if destination:
#             queryset = queryset.filter(destination__icontains=destination)

#         return queryset


# # 2. Flight Details with Live AirLabs Data
# class FlightDetailView(generics.RetrieveAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     lookup_field = 'id'

#     def retrieve(self, request, *args, **kwargs):
#         # Get flight from database
#         instance = self.get_object()

#         serializer = self.get_serializer(instance)
#         flight_data = serializer.data

#         # AirLabs API configuration
#         airlabs_api_key = '7b99c8c6-e786-4557-a7c3-82d44aadb2fe'
#         flight_iata = instance.flight_number

#         try:
#             url = "https://airlabs.co/api/v9/flight"

#             params = {
#                 'flight_iata': flight_iata,
#                 'api_key': airlabs_api_key
#             }

#             # Request live flight data
#             api_response = requests.get(
#                 url,
#                 params=params,
#                 timeout=10
#             )

#             api_response.raise_for_status()

#             result = api_response.json()
#             live_data = result.get('response')

#             if live_data:

#                 flight_data['live_metrics'] = {
#                     # Flight information
#                     'flight_number': live_data.get('flight_iata'),
#                     'status': live_data.get('status'),

#                     # Aircraft location
#                     'latitude': live_data.get('lat'),
#                     'longitude': live_data.get('lng'),

#                     # Aircraft movement
#                     'altitude_meters': live_data.get('alt'),
#                     'speed_kmh': live_data.get('speed'),
#                     'direction': live_data.get('dir'),
#                     'vertical_speed': live_data.get('v_speed'),

#                     # Departure and arrival
#                     'departure': live_data.get('dep_iata'),
#                     'arrival': live_data.get('arr_iata'),

#                     # Estimated arrival
#                     'estimated_arrival': live_data.get('arr_estimated'),

#                     # Flight delay
#                     'delayed_minutes': live_data.get('arr_delayed'),

#                     # Last updated time
#                     'last_updated': live_data.get('updated'),
#                 }

#             else:
#                 flight_data['live_metrics'] = None

#         except requests.RequestException as e:
#             print(f"AirLabs API Error: {e}")
#             flight_data['live_metrics'] = None

#         return Response(flight_data)


# # 3. Admin Flight List and Create
# class AdminFlightListView(generics.ListCreateAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAdminUser]


# # 4. Admin Flight Status Update
# class AdminFlightStatusUpdateView(generics.UpdateAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAdminUser]
#     lookup_field = 'id'



# import requests
# from rest_framework import generics, permissions, status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Flight
# from .serializers import FlightSerializer

# # --- 1. Database Flight Search ---
# class FlightSearchView(generics.ListAPIView):
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         queryset = Flight.objects.all()
        
#         # 1. Location Filters
#         departure = self.request.query_params.get('departure')
#         arrival = self.request.query_params.get('arrival')
#         if departure:
#             queryset = queryset.filter(departure_airport__icontains=departure)
#         if arrival:
#             queryset = queryset.filter(arrival_airport__icontains=arrival)
            
#         # 2. Price and Hours Filters
#         min_price = self.request.query_params.get('min_price')
#         max_price = self.request.query_params.get('max_price')
#         max_hours = self.request.query_params.get('max_hours')
        
#         if min_price:
#             queryset = queryset.filter(price__gte=min_price)
#         if max_price:
#             queryset = queryset.filter(price__lte=max_price)
#         if max_hours:
#             queryset = queryset.filter(travel_hours__lte=max_hours)

#         # 3. Sorting
#         sort_by = self.request.query_params.get('sort_by')
#         sort_order = self.request.query_params.get('sort_order')
        
#         if sort_by in ['price', 'travel_hours']:
#             prefix = '-' if sort_order == 'desc' else ''
#             queryset = queryset.order_by(f'{prefix}{sort_by}')
            
#         return queryset

# # --- 2. Database Flight Detail ---
# class FlightDetailView(generics.RetrieveAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     lookup_field = 'id'

# # --- 3. Admin Flight Management ---
# class AdminFlightListView(generics.ListCreateAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAdminUser]

# class AdminFlightStatusUpdateView(generics.UpdateAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAdminUser]
#     lookup_field = 'id'

# # --- 4. Live Radar Tracking (AirLabs Proxy) ---
# class LiveFlightTrackingView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, flight_iata):
#         # ⚠️ PASTE YOUR ACTUAL API KEY HERE
#         airlabs_api_key = '7b99c8c6-e786-4557-a7c3-82d44aadb2fe' 
        
#         url = f"https://airlabs.co/api/v9/flight?flight_iata={flight_iata}&api_key={airlabs_api_key}"
        
#         try:
#             response = requests.get(url, timeout=5)
#             data = response.json()
            
#             # If AirLabs successfully finds the airborne flight
#             if 'response' in data:
#                 live = data['response']
#                 return Response({
#                     "flight_number": live.get("flight_iata", flight_iata),
#                     "departure_airport": live.get("dep_iata", "N/A"),
#                     "arrival_airport": live.get("arr_iata", "N/A"),
#                     "status": live.get("status", "Unknown"),
#                     "altitude_meters": live.get("alt", 0),
#                     "speed_kmh": live.get("speed", 0),
#                     "delayed": live.get("delayed", 0),
#                     "lat": live.get("lat", 0),
#                     "lng": live.get("lng", 0)
#                 })
                
#             # If AirLabs rejects the request (e.g., bad API key, limit reached, or flight not found)
#             elif 'error' in data:
#                 error_msg = data['error'].get('message', 'Unknown AirLabs Error')
#                 return Response(
#                     {"error": f"AirLabs: {error_msg}"}, 
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
                
#             else:
#                 return Response(
#                     {"error": "Flight not found on radar. It may be grounded."}, 
#                     status=status.HTTP_404_NOT_FOUND
#                 )
                
#         except requests.RequestException:
#             return Response(
#                 {"error": "Failed to connect to AirLabs radar servers."}, 
#                 status=status.HTTP_503_SERVICE_UNAVAILABLE
#             )

#     class LiveFlightSearchView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         airlabs_api_key = 'YOUR_AIRLABS_API_KEY' # Replace with your key
        
#         # AirLabs requires IATA codes (like JFK or LHR)
#         dep = request.query_params.get('departure', '').upper().strip()
#         arr = request.query_params.get('arrival', '').upper().strip()
        
#         if not dep and not arr:
#             return Response(
#                 {"error": "Please enter at least a Departure or Arrival airport IATA code (e.g., JFK, LAX)."}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
            
#         url = f"https://airlabs.co/api/v9/schedules?api_key={airlabs_api_key}"
#         if dep: url += f"&dep_iata={dep}"
#         if arr: url += f"&arr_iata={arr}"
        
#         try:
#             res = requests.get(url, timeout=10)
#             data = res.json()
            
#             if 'error' in data:
#                 return Response({"error": data['error'].get('message', 'AirLabs error')}, status=status.HTTP_400_BAD_REQUEST)
                
#             schedules = data.get('response', [])
#             processed_flights = []
            
#             for s in schedules:
#                 flight_num = s.get('flight_iata') or s.get('flight_icao')
#                 if not flight_num:
#                     continue
                    
#                 # 1. Simulate Price (deterministic based on flight number so it doesn't change randomly)
#                 base_price = sum(ord(c) for c in flight_num) % 400 + 150 
                
#                 # 2. Calculate Travel Hours from AirLabs duration (which is in minutes)
#                 duration_mins = s.get('duration', 0)
#                 if not duration_mins:
#                     duration_mins = (base_price % 300) + 60 # Fallback mock duration
#                 travel_hours = round(duration_mins / 60, 2)
                
#                 processed_flights.append({
#                     "flight_number": flight_num,
#                     "departure_airport": s.get('dep_iata', dep),
#                     "arrival_airport": s.get('arr_iata', arr),
#                     "departure_time": s.get('dep_time_utc', 'Scheduled'),
#                     "status": s.get('status', 'scheduled'),
#                     "price": float(base_price),
#                     "travel_hours": float(travel_hours)
#                 })
                
#             # 3. Apply Filters from React
#             min_price = float(request.query_params.get('min_price') or 0)
#             max_price = float(request.query_params.get('max_price') or 99999)
#             max_hours = float(request.query_params.get('max_hours') or 999)
            
#             filtered_flights = [
#                 f for f in processed_flights
#                 if min_price <= f['price'] <= max_price
#                 and f['travel_hours'] <= max_hours
#             ]
            
#             # 4. Apply Sorting from React
#             sort_by = request.query_params.get('sort_by', 'price')
#             sort_order = request.query_params.get('sort_order', 'asc')
#             reverse_order = (sort_order == 'desc')
            
#             if sort_by in ['price', 'travel_hours']:
#                 filtered_flights.sort(key=lambda x: x[sort_by], reverse=reverse_order)
                
#             # Return top 50 results to prevent massive payloads
#             return Response(filtered_flights[:50])
            
#         except Exception as e:
#             return Response({"error": "Failed to fetch live schedules from AirLabs."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)




# import requests
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework import generics, permissions, status
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .models import Flight
# from .serializers import FlightSerializer

# # --- 1. Database Flight Search (Legacy/Optional) ---
# class FlightSearchView(generics.ListAPIView):
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         queryset = Flight.objects.all()
        
#         departure = self.request.query_params.get('departure')
#         arrival = self.request.query_params.get('arrival')
#         if departure:
#             queryset = queryset.filter(departure_airport__icontains=departure)
#         if arrival:
#             queryset = queryset.filter(arrival_airport__icontains=arrival)
            
#         min_price = self.request.query_params.get('min_price')
#         max_price = self.request.query_params.get('max_price')
#         max_hours = self.request.query_params.get('max_hours')
        
#         if min_price:
#             queryset = queryset.filter(price__gte=min_price)
#         if max_price:
#             queryset = queryset.filter(price__lte=max_price)
#         if max_hours:
#             queryset = queryset.filter(travel_hours__lte=max_hours)

#         sort_by = self.request.query_params.get('sort_by')
#         sort_order = self.request.query_params.get('sort_order')
        
#         if sort_by in ['price', 'travel_hours']:
#             prefix = '-' if sort_order == 'desc' else ''
#             queryset = queryset.order_by(f'{prefix}{sort_by}')
            
#         return queryset

# # --- 2. Database Flight Detail ---
# class FlightDetailView(generics.RetrieveAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     lookup_field = 'id'

# # --- 3. Admin Flight Management ---
# class AdminFlightListView(generics.ListCreateAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAdminUser]

# class AdminFlightStatusUpdateView(generics.UpdateAPIView):
#     queryset = Flight.objects.all()
#     serializer_class = FlightSerializer
#     permission_classes = [permissions.IsAdminUser]
#     lookup_field = 'id'

# # --- 4. Live Radar Tracking (AirLabs Proxy) ---
# class LiveFlightTrackingView(APIView):
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request, flight_iata):
#         airlabs_api_key = '7b99c8c6-e786-4557-a7c3-82d44aadb2fe' 
        
#         url = f"https://airlabs.co/api/v9/flight?flight_iata={flight_iata}&api_key={airlabs_api_key}"
        
#         try:
#             response = requests.get(url, timeout=5)
#             data = response.json()
            
#             if 'response' in data:
#                 live = data['response']
#                 return Response({
#                     "flight_number": live.get("flight_iata", flight_iata),
#                     "departure_airport": live.get("dep_iata", "N/A"),
#                     "arrival_airport": live.get("arr_iata", "N/A"),
#                     "status": live.get("status", "Unknown"),
#                     "altitude_meters": live.get("alt", 0),
#                     "speed_kmh": live.get("speed", 0),
#                     "delayed": live.get("delayed", 0),
#                     "lat": live.get("lat", 0),
#                     "lng": live.get("lng", 0)
#                 })
#             elif 'error' in data:
#                 error_msg = data['error'].get('message', 'Unknown AirLabs Error')
#                 return Response(
#                     {"error": f"AirLabs: {error_msg}"}, 
#                     status=status.HTTP_400_BAD_REQUEST
#                 )
#             else:
#                 return Response(
#                     {"error": "Flight not found on radar. It may be grounded."}, 
#                     status=status.HTTP_404_NOT_FOUND
#                 )
                
#         except requests.RequestException:
#             return Response(
#                 {"error": "Failed to connect to AirLabs radar servers."}, 
#                 status=status.HTTP_503_SERVICE_UNAVAILABLE
#             )

# # --- 5. Live Schedule Search with Filters & Sorting (AirLabs Proxy) ---

# class LiveFlightSearchView(APIView):
#     authentication_classes = [JWTAuthentication] # <--- Add this line
#     permission_classes = [permissions.IsAuthenticated]

#     def get(self, request):
#         airlabs_api_key = '7b99c8c6-e786-4557-a7c3-82d44aadb2fe' 
        
#         dep = request.query_params.get('departure', '').upper().strip()
#         arr = request.query_params.get('arrival', '').upper().strip()
        
#         if not dep and not arr:
#             return Response(
#                 {"error": "Please enter at least a Departure or Arrival airport IATA code (e.g., JFK, LAX)."}, 
#                 status=status.HTTP_400_BAD_REQUEST
#             )
            
#         url = f"https://airlabs.co/api/v9/schedules?api_key={airlabs_api_key}"
#         if dep: url += f"&dep_iata={dep}"
#         if arr: url += f"&arr_iata={arr}"
        
#         try:
#             res = requests.get(url, timeout=10)
#             data = res.json()
            
#             if 'error' in data:
#                 return Response({"error": data['error'].get('message', 'AirLabs error')}, status=status.HTTP_400_BAD_REQUEST)
                
#             schedules = data.get('response', [])
#             processed_flights = []
            
#             for s in schedules:
#                 flight_num = s.get('flight_iata') or s.get('flight_icao')
#                 if not flight_num:
#                     continue
                    
#                 base_price = sum(ord(c) for c in flight_num) % 400 + 150 
                
#                 duration_mins = s.get('duration', 0)
#                 if not duration_mins:
#                     duration_mins = (base_price % 300) + 60 
#                 travel_hours = round(duration_mins / 60, 2)
                
#                 processed_flights.append({
#                     "flight_number": flight_num,
#                     "departure_airport": s.get('dep_iata', dep),
#                     "arrival_airport": s.get('arr_iata', arr),
#                     "departure_time": s.get('dep_time_utc', 'Scheduled'),
#                     "status": s.get('status', 'scheduled'),
#                     "price": float(base_price),
#                     "travel_hours": float(travel_hours)
#                 })
                
#             min_price = float(request.query_params.get('min_price') or 0)
#             max_price = float(request.query_params.get('max_price') or 99999)
#             max_hours = float(request.query_params.get('max_hours') or 999)
            
#             filtered_flights = [
#                 f for f in processed_flights
#                 if min_price <= f['price'] <= max_price
#                 and f['travel_hours'] <= max_hours
#             ]
            
#             sort_by = request.query_params.get('sort_by', 'price')
#             sort_order = request.query_params.get('sort_order', 'asc')
#             reverse_order = (sort_order == 'desc')
            
#             if sort_by in ['price', 'travel_hours']:
#                 filtered_flights.sort(key=lambda x: x[sort_by], reverse=reverse_order)
                
#             return Response(filtered_flights[:50])
            
#         except Exception as e:
#             return Response({"error": "Failed to fetch live schedules from AirLabs."}, status=status.HTTP_503_SERVICE_UNAVAILABLE)




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