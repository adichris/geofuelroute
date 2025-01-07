from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import openrouteservice
from .models import FuelStation
from .serializers import DestinationSerializer
from django.conf import settings


class CalculateRouteView(APIView):
    serializer_class = DestinationSerializer

    def get(self, request):
        """
        GET method provides a description of the API and how to use it.
        """
        return Response({
            "message": "This route calculate Fuel Cost for a destination",
            "usage": {
                "method": "POST",
                "endpoint": "/api/",
                "parameters": {
                    "start_lat": "Latitude of the starting point (float)",
                    "start_lng": "Longitude of the starting point (float)",
                    "end_lat": "Latitude of the ending point (float)",
                    "end_lng": "Longitude of the ending point (float)"
                },
                "example_request": {
                    "start_lat": 38.9072,
                    "start_lng": -77.0369,
                    "end_lat": 40.7128,
                    "end_lng": -74.0060
                },
                "response_format": {
                    "total_distance_miles": "Total distance of the route in miles (float)",
                    "total_fuel_required_gallons": "Total fuel required in gallons (float)",
                    "total_cost": "Total cost of fuel in USD (float)",
                    "stops": "List of fuel stops along the route",
                    "route_geometry": "Route geometry for visualization"
                }
            }
        }, status=status.HTTP_200_OK)

    def post(self, request):
        # Validate input using serializer
        serializer = DestinationSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Extract validated data
        data = serializer.validated_data
        start_lat, start_lng = data['start_lat'], data['start_lng']
        end_lat, end_lng = data['end_lat'], data['end_lng']

        # Vehicle parameters
        fuel_efficiency = 10  # miles per gallon
        tank_range = 500  # miles
        fuel_capacity = tank_range / fuel_efficiency  # gallons per tank

        # Initialize OpenRouteService client
        client = openrouteservice.Client(key=settings.OPEN_ROUTE_SERVICE_API)

        # Get the route from OpenRouteService
        try:
            route = client.directions(
                coordinates=[[start_lng, start_lat], [end_lng, end_lat]],
                profile="driving-car",
                format="geojson"
            )
        except openrouteservice.exceptions.ApiError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Extract route distance (in meters) and convert to miles
        total_distance_meters = route["features"][0]["properties"]["segments"][0]["distance"]
        total_distance_miles = total_distance_meters * 0.000621371

        # Calculate total fuel required
        total_fuel_required = total_distance_miles / fuel_efficiency

        # Calculate required fuel stops
        fuel_stops = int(total_distance_miles // tank_range)

        # Query fuel stations along the route (example assumes all stations are valid)
        fuel_stations = FuelStation.objects.order_by('retail_price')[:fuel_stops + 1]

        # Calculate fuel costs and stops
        total_cost = 0
        stops = []
        for i, station in enumerate(fuel_stations):
            gallons_needed = fuel_capacity if i < fuel_stops else total_fuel_required % fuel_capacity
            cost = float(gallons_needed) * float(station.retail_price)
            total_cost += cost
            stops.append({
                "opis_trucking_id": station.opis_trucking_id,
                "truckstop_name": station.truckstop_name,
                "address":station.address,
                "city": station.city,
                "state": station.state,
                "price_per_gallon": station.retail_price,
                "gallons_needed": round(gallons_needed, 2),
                "cost": round(cost, 2)
            })

        # Response
        response = {
            "total_distance_miles": round(total_distance_miles, 2),
            "total_fuel_required_gallons": round(total_fuel_required, 2),
            "total_cost": round(total_cost, 2),
            "stops": stops,
            "route_geometry": route["features"][0]["geometry"]
        }

        return Response(response, status=status.HTTP_200_OK)

