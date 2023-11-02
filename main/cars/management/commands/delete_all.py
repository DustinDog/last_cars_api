from cars.models import Brand, Car, Model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    def handle(self, **options):
        Car.objects.all().delete()

        Model.objects.all().delete()

        Brand.objects.all().delete()

        print("Successfully deleted all instances in the database")
