from django.core.management.base import BaseCommand
from faker import Faker
from faker_vehicle import VehicleProvider
from cars.models import Brand, Model, Car

from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("count", type=int)

    def handle(self, **options):
        fake = Faker()
        fake.add_provider(VehicleProvider)
        count = options["count"]
        fuels = ["gasoline", "diesel", "electric", "hybrid"]
        transmissions = ["automatic", "manual"]
        engines = ["2.0L", "1.4L", "3.0L", "5.0L"]

        for _ in range(count):
            brand = Brand.objects.create(
                name=fake.vehicle_make(),
                headquarters_country=fake.country(),
            )

            model = Model.objects.create(
                name=fake.vehicle_model(),
                year_of_issue=fake.machine_year(),
                body_style=fake.vehicle_category(),
                brand=brand,
            )
            user, created = User.objects.get_or_create(
                email="user@user.com",
            )
            if created:
                user.set_password("password")
            Car.objects.create(
                title="BMV",
                description="Nice new car",
                brand=brand,
                model=model,
                price=f"{fake.pyint()}USD",
                mileage=f"{fake.pyint()}kilometers",
                exterior_color=fake.safe_color_name(),
                interior_color=fake.safe_color_name(),
                fuel_type=fake.random_element(elements=fuels),
                transmission=fake.random_element(elements=transmissions),
                engine=fake.random_element(elements=engines),
                is_on_sale=fake.boolean(),
                user=user,
            )

        print(f"Successfully generated {count} cars")
