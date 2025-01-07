from django.contrib import admin
from .models import FuelStation


@admin.register(FuelStation)
class FuelStationAdmin(admin.ModelAdmin):
    list_display = ["opis_trucking_id", "truckstop_name", "address", "city", "state", "rack_id", "retail_price"]
    list_max_show_all = 200
    list_filter = ["state"]
    list_per_page = 100
    search_fields = ["city", "state", "address"]
    search_help_text = "city, state, or address"

