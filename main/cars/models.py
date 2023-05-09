from django.db import models
from cars.utils import build_path
from django.contrib.auth import get_user_model


User = get_user_model()


class Brand(models.Model):
    name = models.CharField(max_length=50)
    headquarters_country = models.CharField(max_length=150)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"


class Model(models.Model):
    name = models.CharField(max_length=50)
    year_of_issue = models.PositiveIntegerField()
    body_style = models.CharField(max_length=50)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Model"
        verbose_name_plural = "Models"


class Car(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="cars")
    model = models.ForeignKey(Model, on_delete=models.CASCADE, related_name="cars")
    price = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="cars")

    """Not required"""
    is_on_sale = models.BooleanField(default=True)
    engine = models.CharField(max_length=50, blank=True, null=True)
    mileage = models.CharField(max_length=150, blank=True, null=True)
    exterior_color = models.CharField(max_length=150, blank=True, null=True)
    interior_color = models.CharField(max_length=150, blank=True, null=True)
    fuel_type = models.CharField(max_length=150, blank=True, null=True)
    transmission = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return f"{self.brand.name} {self.model.name} ({self.is_on_sale})"

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"


class CarImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=build_path)

    def __str__(self):
        return f"{self.car} - {self.image.name}"
