import requests
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Flight
from .serializers import FlightSerializer, FlightStatusUpdateSerializer

AIRLABS_API_KEY = '7b99c8c6-e786-4557-a7c3-82d44aadb2fe'
VALID_FLIGHT_STATUSES = {'Scheduled', 'Delayed', 'Boarding', 'Cancelled', 'Landed'}


def _normalize_status(raw_status):
    cleaned = (raw_status or 'Scheduled').strip().capitalize()
    return cleaned if cleaned in VALID_FLIGHT_STATUSES else 'Scheduled'




def _fetch_and_sync_airlabs_schedules(dep='', arr=''):
    """
    Fetches live schedules from AirLabs, syncs new flights into `Flight`,
    and applies any admin-updated `Flight.status` from the database.
    """
    url = f"https://airlabs.co/api/v9/schedules?api_key={AIRLABS_API_KEY}"
    if dep:
        url += f"&dep_iata={dep}"
    if arr:
        url += f"&arr_iata={arr}"

    res = requests.get(url, timeout=10)
    data = res.json()

    if 'error' in data:
        raise ValueError(data['error'].get('message', 'AirLabs error'))

    schedules = data.get('response', [])
    processed_flights = []

    for s in schedules:
        flight_num = s.get('flight_iata') or s.get('flight_icao')
        dep_iata = s.get('dep_iata') or dep
        arr_iata = s.get('arr_iata') or arr
        if not flight_num or not dep_iata or not arr_iata:
            continue

        base_price = sum(ord(c) for c in flight_num) % 400 + 150
        duration_mins = s.get('duration', 0)
        if not duration_mins:
            duration_mins = (base_price % 300) + 60
        travel_hours = round(duration_mins / 60, 2)
        dep_time = s.get('dep_time_utc') or s.get('dep_time') or 'Scheduled'
        airlabs_status = _normalize_status(s.get('status'))

        flight_obj, created = Flight.objects.get_or_create(
            flight_number=flight_num,
            departure_airport=dep_iata,
            arrival_airport=arr_iata,
            defaults={
                'departure_time': dep_time,
                'status': airlabs_status,
                'price': float(base_price),
                'travel_hours': float(travel_hours),
                'available_seats': 18,
            },
        )

        # Keep admin status updates in the DB; only update departure_time/price/hours
        if not created:
            flight_obj.departure_time = dep_time
            flight_obj.price = float(base_price)
            flight_obj.travel_hours = float(travel_hours)
            flight_obj.save(update_fields=['departure_time', 'price', 'travel_hours', 'updated_at'])

        processed_flights.append({
            'id': flight_obj.id,
            'flight_number': flight_obj.flight_number,
            'departure_airport': flight_obj.departure_airport,
            'arrival_airport': flight_obj.arrival_airport,
            'departure_time': flight_obj.departure_time,
            'status': flight_obj.status,
            'price': float(flight_obj.price),
            'travel_hours': float(flight_obj.travel_hours),
            'available_seats': flight_obj.available_seats,
        })

    return processed_flights


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
class AdminFlightListView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = FlightSerializer

    def get_queryset(self):
        dep = self.request.query_params.get('departure', 'CCJ').upper().strip() or 'CCJ'
        arr = self.request.query_params.get('arrival', '').upper().strip()

        if not Flight.objects.exists() or self.request.query_params.get('sync') == 'true':
            try:
                _fetch_and_sync_airlabs_schedules(dep=dep, arr=arr)
            except Exception as exc:
                print(f"AirLabs sync skipped: {exc}")

        qs = Flight.objects.all().order_by('id')
        flight_status = self.request.query_params.get('status')
        if flight_status and flight_status != 'All':
            qs = qs.filter(status__iexact=flight_status)
        return qs


class AdminFlightStatusUpdateView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def put(self, request, pk):
        try:
            flight = Flight.objects.get(pk=pk)
        except Flight.DoesNotExist:
            return Response({'error': 'Flight not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = FlightStatusUpdateSerializer(flight, data=request.data, partial=True)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(FlightSerializer(flight).data, status=status.HTTP_200_OK)


# --- 4. Live Radar Tracking (AirLabs Proxy) ---
class LiveFlightTrackingView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, flight_iata):
        url = f"https://airlabs.co/api/v9/flight?flight_iata={flight_iata}&api_key={AIRLABS_API_KEY}"

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


        


class LiveFlightSearchView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        dep = request.query_params.get('departure', '').upper().strip()
        arr = request.query_params.get('arrival', '').upper().strip()

        if not dep and not arr:
            return Response(
                {"error": "Please enter at least a Departure or Arrival airport IATA code (e.g., CCJ, COK)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            processed_flights = _fetch_and_sync_airlabs_schedules(dep=dep, arr=arr)

            min_price = float(request.query_params.get('min_price') or 0)
            max_price = float(request.query_params.get('max_price') or 99999)
            max_hours = float(request.query_params.get('max_hours') or 999)
            min_seats = int(request.query_params.get('min_seats') or 1)
            travel_date = (request.query_params.get('date') or '').strip()
            status_filter = (request.query_params.get('status') or '').strip().lower()

            bookable_group = {'scheduled', 'delayed', 'boarding', 'on-time', 'upcoming', 'available'}

            filtered_flights = []
            for f in processed_flights:
                current_status = (f.get('status') or 'Scheduled').strip().lower()

                if not (min_price <= f['price'] <= max_price):
                    continue
                if f['travel_hours'] > max_hours:
                    continue
                if (f.get('available_seats') or 18) < min_seats:
                    continue
                if travel_date and not str(f.get('departure_time') or '').startswith(travel_date):
                    continue

                if status_filter and status_filter != 'all':
                    if status_filter == 'scheduled':
                        if current_status not in bookable_group:
                            continue
                    elif current_status != status_filter:
                        continue

                filtered_flights.append(f)

            sort_by = request.query_params.get('sort_by', 'price')
            sort_order = request.query_params.get('sort_order', 'asc')
            reverse_order = (sort_order == 'desc')

            if sort_by in ['price', 'travel_hours']:
                filtered_flights.sort(key=lambda x: x[sort_by], reverse=reverse_order)

            return Response(filtered_flights[:50])

        except ValueError as err:
            return Response({"error": str(err)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                {"error": "Failed to fetch live schedules from AirLabs."},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )