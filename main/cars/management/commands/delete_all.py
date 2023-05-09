from django.core.management.base import BaseCommand
from cars.models import Brand, Model, Car


class Command(BaseCommand):
    def handle(self, **options):
        Car.objects.all().delete()

        Model.objects.filter(car__isnull=True).delete()

        Brand.objects.filter(model__isnull=True).delete()

        print("Successfully deleted all instances in the database")
