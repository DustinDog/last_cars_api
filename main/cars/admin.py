from django.contrib import admin

from cars.models import Brand, Car, CarImage, Model

admin.site.register(Brand)
admin.site.register(Model)
admin.site.register(Car)
admin.site.register(CarImage)
