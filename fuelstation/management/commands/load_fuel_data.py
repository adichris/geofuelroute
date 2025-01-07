import csv
from django.core.management.base import BaseCommand, CommandError
from fuelstation.models import FuelStation
import os

class Command(BaseCommand):
    help = "Load fuel data from a CSV file into fuelstation database table"

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str)

    def handle(self, *args, **options):
        file_path = options["file_path"]
        if file_path and os.path.isfile(file_path):
            with open(file_path, 'r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    FuelStation.objects.update_or_create(
                        opis_trucking_id=row['OPIS Truckstop ID'],
                        defaults={
                            'truckstop_name': row['Truckstop Name'],
                            'address': row['Address'],
                            'city': row['City'],
                            'state': row['State'],
                            'rack_id': row['Rack ID'],
                            'retail_price': row['Retail Price']
                        }
                    )
            self.stdout.write(self.style.SUCCESS("Fuel data loaded successfully!"))
        else:
            self.stdout.write(self.style.ERROR("expected path a csv file"))