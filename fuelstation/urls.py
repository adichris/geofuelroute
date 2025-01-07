from rest_framework import routers
from .views import CalculateRouteView
from django.urls import path


app_name = "fuelstation"
urlpatterns = [
    path("", CalculateRouteView.as_view(), name="calculate_route"),
]

