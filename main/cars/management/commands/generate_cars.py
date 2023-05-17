import os
from django.core.management.base import BaseCommand
import random
from cars.models import Brand, Model, Car, CarImage
from django.contrib.auth import get_user_model
from fixtures.car_examples_dict import CAR_SAMPLE
from django.core.files import File
from django.conf import settings


User = get_user_model()


class Command(BaseCommand):
    def handle(self, **options):
        brand_list = []
        model_list = []
        car_list = []
        car_image_list = []

        fuels = ["gasoline", "diesel", "electric", "hybrid"]
        transmissions = ["automatic", "manual"]
        engines = ["2.0L", "1.4L", "3.0L", "5.0L"]
        vehicles = CAR_SAMPLE
        colors = ["red", "black", "white", "yellow"]
        user, created = User.objects.get_or_create(
            email="gen@gen.com",
        )
        if created:
            user.set_password("password")
            user.save()

        for vehicle in vehicles:
            brand = Brand(
                name=vehicle["brand"],
                headquarters_country=vehicle["country"],
            )
            brand_list.append(brand)
            for vehicle_model in vehicle["models"]:
                model = Model(
                    name=vehicle_model["name"],
                    body_style=vehicle_model["body_type"],
                    brand=brand,
                )
                model_list.append(model)

                car = Car(
                    title="Car title",
                    description="Car description",
                    brand=brand,
                    model=model,
                    year=random.randint(1990, 2023),
                    condition=random.choice(["new", "used"]),
                    price=random.randint(1000, 10000),
                    mileage=random.randint(10, 100) * 100,
                    exterior_color=random.choice(colors),
                    interior_color=random.choice(colors),
                    fuel_type=random.choice(fuels),
                    transmission=random.choice(transmissions),
                    engine=random.choice(engines),
                    is_on_sale=random.choice([True, False]),
                    user=user,
                )
                car_list.append(car)

                filename = os.path.join(settings.BASE_DIR, "static/images/Cruiser.jpg")

                image_file = File(open(filename, "rb"), "car.jpg")
                car_image = CarImage(car=car, image=image_file)
                car_image_list.append(car_image)

        Brand.objects.bulk_create(brand_list)
        Model.objects.bulk_create(model_list)
        Car.objects.bulk_create(car_list)
        CarImage.objects.bulk_create(car_image_list)
        print(f"Successfully generated 15 cars")
