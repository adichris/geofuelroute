from django.db import models


class FuelStation(models.Model):
    opis_trucking_id = models.IntegerField(unique=True)  # Unique identifier for each station
    truckstop_name = models.CharField(max_length=255)  # Name of the fuel station
    address = models.CharField(max_length=255)  # Address of the station
    city = models.CharField(max_length=100)  # City where the station is located
    state = models.CharField(max_length=2)  # State abbreviation
    rack_id = models.IntegerField()  # Rack ID for categorization
    retail_price = models.DecimalField(max_digits=5, decimal_places=3)  # Price per gallon
    
    def __str__(self):
        return f"{self.truckstop_name} ({self.city}, {self.state})"

