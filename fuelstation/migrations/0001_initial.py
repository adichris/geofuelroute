# Generated by Django 5.1.4 on 2025-01-07 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FuelStation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("opis_trucking_id", models.IntegerField(unique=True)),
                ("truckstop_name", models.CharField(max_length=255)),
                ("address", models.CharField(max_length=255)),
                ("city", models.CharField(max_length=100)),
                ("state", models.CharField(max_length=2)),
                ("rack_id", models.IntegerField()),
                ("retail_price", models.DecimalField(decimal_places=3, max_digits=5)),
            ],
        ),
    ]
