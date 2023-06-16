# Generated by Django 4.2.1 on 2023-05-16 12:59

import re

from django.db import migrations, models


def remove_letters_from_price(apps, schema_editor):
    Car = apps.get_model("cars", "Car")
    for car in Car.objects.all():
        string_with_letters = car.price
        string_without_letters = re.sub("[a-zA-Z]+", "", string_with_letters)
        try:
            car.price = int(string_without_letters)
            car.mileage = re.sub("[a-zA-Z]+", "", car.mileage)
            car.save()
        except Exception as e:
            print("error: ", str(e))
            car.price = 1000
            car.mileage = 10000
            car.save()


class Migration(migrations.Migration):
    dependencies = [
        ("cars", "0004_remove_model_year_of_issue"),
    ]

    operations = [
        migrations.RunPython(remove_letters_from_price, elidable=True),
        migrations.AlterField(
            model_name="car",
            name="mileage",
            field=models.PositiveIntegerField(blank=True, null=True, default=0),
        ),
        migrations.AlterField(
            model_name="car",
            name="price",
            field=models.PositiveIntegerField(),
        ),
    ]
