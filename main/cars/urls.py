from django.urls import path

from cars.views import (
    BrandListAPIView,
    ModelListAPIView,
    CarListCreateAPIView,
    DeleteCarByIdAPIView,
)

urlpatterns = [
    path("", CarListCreateAPIView.as_view(), name="list_create"),
    path("brands/", BrandListAPIView.as_view(), name="brand_list"),
    path("models/", ModelListAPIView.as_view(), name="model_list"),
    path("<int:pk>/", DeleteCarByIdAPIView.as_view(), name="delete_car"),
]
